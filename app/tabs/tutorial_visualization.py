"""Tab 1: Interactive data visualization with widgets"""

import hvplot.pandas
import pandas as pd
import panel as pn
from panel_exploration.app.layout import PRIMARY_COLOR, SECONDARY_COLOR, CSV_FILE


@pn.cache
def get_data():
    return pd.read_csv(CSV_FILE, parse_dates=["date"], index_col="date")


def transform_data(variable, window, sigma):
    """Calculates the rolling average and identifies outliers"""
    data = get_data()
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = abs(residual) > std * sigma
    return avg, avg[outliers]


def get_plot(variable="Temperature", window=30, sigma=10):
    """Plots the rolling average and the outliers"""
    avg, highlight = transform_data(variable, window, sigma)
    return avg.hvplot(
        height=300, legend=False, color=PRIMARY_COLOR
    ) * highlight.hvplot.scatter(color=SECONDARY_COLOR, padding=0.1, legend=False)


def create_viz_tab():
    """Create the data visualization tab"""
    data = get_data()
    
    # Widgets
    variable_widget = pn.widgets.Select(
        name="variable", value="Temperature", options=list(data.columns)
    )
    window_widget = pn.widgets.IntSlider(name="window", value=30, start=1, end=60)
    sigma_widget = pn.widgets.IntSlider(name="sigma", value=10, start=0, end=20)
    
    # Bind plot to widgets
    bound_plot = pn.bind(
        get_plot, variable=variable_widget, window=window_widget, sigma=sigma_widget
    )
    
    return pn.Column(
        "## Interactive Data Visualization",
        "Adjust the parameters below to see how the rolling average and outliers change.",
        pn.Row(variable_widget, window_widget, sigma_widget),
        bound_plot,
        "Resource: https://panel.holoviz.org/getting_started/build_app.html"
    )