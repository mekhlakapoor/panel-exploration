"""Tab modules for the Panel playground app"""

from panel_exploration.app.tabs.tutorial_visualization import create_viz_tab
from panel_exploration.app.tabs.hello_world import create_hello_world_tab 
from panel_exploration.app.tabs.docdb_explorer import create_docdb_tab
from panel_exploration.app.tabs.s3_explorer import create_s3_tab

__all__ = [
    "create_viz_tab",
    "create_hello_world_tab",
    "create_docdb_tab",
    "create_s3_tab",
]