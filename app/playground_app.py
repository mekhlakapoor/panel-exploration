"""Main Panel playground app combining all exploration tabs"""

import panel as pn
from panel_exploration.app.tabs import (
    create_viz_tab,
    create_hello_world_tab,
    create_docdb_tab,
    create_s3_tab,
)


pn.extension(design="material", sizing_mode="stretch_width")

tabs = pn.Tabs(
    ("Data Visualization Tutorial", create_viz_tab()),
    ("Hello World", create_hello_world_tab()),
    ("DocDB Explorer", create_docdb_tab),
    ("S3 Explorer", create_s3_tab()),
)

pn.template.MaterialTemplate(
    site="Panel Playground",
    title="Exploration and Demos",
    main=[tabs],
).servable()