# Panel Framework Exploration

This project documents my journey learning the Panel framework to prepare for contributing to [aind-qc-portal](https://github.com/AllenNeuralDynamics/aind-qc-portal).

## Project Goal

Build foundational knowledge of Panel framework patterns and AWS infrastructure (DocDB + S3) used in the QC Portal, with a focus on:
- Understanding Panel's reactive programming model
- Connecting to AWS services (S3 and DocDB) in containerized environments
- Learning PyComponent patterns for building reusable UI components

## What This Exploration Covers

### Core Panel Concepts
- **Three Programming APIs**: Reactive (pn.bind), Declarative (Parameterized classes), Callbacks (manual event handlers)
- **Layout Components**: Column, Row, Tabs, Accordion
- **Widgets**: Select, MultiChoice, TextInput, Button
- **Display Panes**: Markdown, Image, Video, PDF, JSON

### Infrastructure Connections
- **DocDB**: Using `aind-data-access-api.document_db.MetadataDbClient` to query metadata
- **S3**: Using `boto3` with for secure media access
- **Docker**: Containerized app with AWS credential mounting

## Project Structure

```
panel_exploration/
├── app/
│   ├── playground_app.py          # Main multi-tab 
│   ├── layout.py                  # Shared 
│   └── tabs/
│       ├── tutorial_visualization.py  # Data viz with widgets (Declarative API)
│       ├── hello_world.py            # Simple callbacks (Callbacks API)
│       ├── docdb_explorer.py         # DocDB connection demo
│       └── s3_explorer.py            # S3 + presigned URLs demo
├── notebooks/
│   └── 01_getting_started/       # Jupyter notebook tutorial
├── Dockerfile                     # Containerized deployment
├── requirements.txt
├── NOTES.md                       # Detailed exploration notes
└── README.md
```

## Running the App

### Local Development
```bash
pip install -r requirements.txt
panel serve app/playground_app.py --show --autoreload
```

### Docker (with AWS credentials)
```bash
# Build
docker build -t panel-playground .

# Run with AWS credentials mounted
docker run -p 5006:5006 \
    -v $USERPROFILE/.aws:/root/.aws:ro \
    -e AWS_PROFILE=dev \
    panel-playground
```

**Note**: On Git Bash for Windows, use `MSYS_NO_PATHCONV=1` to prevent path conversion issues.

## Next Steps: QC Portal Contributions

See `NOTES.md` for:
- QC Portal architecture analysis
- Issues encountered during local setup
- Proposed improvements and fixes

## Resources
- [Panel Documentation](https://panel.holoviz.org/)
- [Panel APIs Explanation](https://panel.holoviz.org/explanation/api/index.html)
- [Param Documentation](https://param.holoviz.org/)
- [aind-qc-portal](https://github.com/AllenNeuralDynamics/aind-qc-portal)