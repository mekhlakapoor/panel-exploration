"""Tab 2: Hello World tab with simple button click interaction"""

import panel as pn


def create_hello_world_tab():
    """Create the hello world tab"""
    text_input = pn.widgets.TextInput(name='Your name', placeholder='Enter name here...')
    button = pn.widgets.Button(name='Submit', button_type='primary')
    output = pn.pane.Markdown('')
    
    def on_click(event):
        output.object = f'Hello, **{text_input.value}**!'
    
    button.on_click(on_click)
    
    return pn.Column(
        "## Hello World",
        "Enter your name and click the Submit button.",
        text_input,
        button,
        output,
    )