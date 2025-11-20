"""Tab 3: DocDB connection using AIND's MetadataDbClient"""

import panel as pn
import param
from aind_data_access_api.document_db import MetadataDbClient

class DocDBExplorer(pn.custom.PyComponent):
    """
    Connects to DocDB using MetadataDbClient
    Pattern: PyComponent with params and callbacks
    """
    project_name = param.List(default=[])
    subject_id = param.String(default="")
    
    def __init__(self, **params):
        super().__init__(**params)
        self.client = MetadataDbClient(
            host="api.allenneuraldynamics.org",
            version="v2",
        )
        self._status_pane = pn.pane.Markdown("Ready to query...")
        self._results_pane = pn.pane.JSON({}, depth=2, theme="light")
        self._count_pane = pn.pane.Markdown("**Records found:** 0")
        
        self.param.watch(self._update_query, ['project_name', 'subject_id'])
    
    def _build_query(self):
        """Build MongoDB query from current parameters"""
        query = {}
        if self.project_name:
            query["data_description.project_name"] = {"$in": self.project_name}
        if self.subject_id:
            query["subject.subject_id"] = self.subject_id
        return query
    
    def _update_query(self, event):
        """Callback when parameters change"""
        query = self._build_query()
        
        if not query:
            self._status_pane.object = "Enter search criteria above..."
            self._results_pane.object = {}
            self._count_pane.object = "**Records found:** 0"
            return
        
        try:
            self._status_pane.object = "Querying DocDB..."
            records = self.client.retrieve_docdb_records(
                filter_query=query,
                projection={"name": 1, "subject.subject_id": 1, "data_description.project_name": 1},
                limit=10
            )
            count = len(records)
            self._count_pane.object = f"**Records found:** {count} (showing max 10)"
            self._results_pane.object = records
            self._status_pane.object = "Query successful"
            
        except Exception as e:
            self._status_pane.object = f"Error: {str(e)}"
            self._results_pane.object = {}
            self._count_pane.object = "**Records found:** 0"
    
    def __panel__(self):
        return pn.Column(
            self._status_pane,
            self._count_pane,
            pn.layout.Divider(),
            self._results_pane,
        )


def create_docdb_tab():
    """Create the DocDB connection tab"""
    docdb_explorer = DocDBExplorer()
    
    project_select = pn.widgets.MultiChoice(
        name="Project Names",
        options=["Learning mFISH task", "Ephys Platform", "Behavior Platform"],
        value=[]
    )
    
    subject_input = pn.widgets.TextInput(
        name="Subject ID (optional)",
        placeholder="e.g., 123456"
    )
    
    query_button = pn.widgets.Button(name="Search DocDB", button_type="primary")
    
    def on_query(event):
        docdb_explorer.project_name = project_select.value
        docdb_explorer.subject_id = subject_input.value
    
    query_button.on_click(on_query)
    
    return pn.Column(
        "## DocDB Connection (AIND Pattern)",
        """
        This demonstrates connecting to DocDB using AIND's `MetadataDbClient`.
        """,
        pn.Row(
            pn.Column(
                "### Query Builder",
                project_select,
                subject_input,
                query_button,
                width=400
            ),
            pn.Column(
                "### Results",
                docdb_explorer,
                sizing_mode="stretch_width"
            )
        ),
    )