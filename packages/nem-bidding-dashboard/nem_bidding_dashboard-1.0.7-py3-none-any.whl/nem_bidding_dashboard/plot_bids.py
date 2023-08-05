"""
This program runs a Dash application displaying info about the National
Electricity Market (NEM).
"""

from datetime import datetime, timedelta
from typing import List, Tuple

import dash
from nem_bidding_dashboard import layout_template
import plotly.graph_objects as go
from nem_bidding_dashboard.create_plots import (
    DISPATCH_COLUMNS,
    add_demand_trace,
    add_duid_dispatch_data,
    add_region_dispatch_data,
    adjust_fig_layout,
    get_duid_station_options,
    plot_bids,
    update_colorbar_length,

)
from dash import Dash, Input, Output, State
from plotly.graph_objects import Figure
from nem_bidding_dashboard.query_functions_for_dashboard import unit_types

app = Dash(__name__)
app.title = "NEM Bidding Dashboard"

application = app.server
app.layout = layout_template.call


@app.callback(
    dash.dependencies.Output("start-date-picker", "date"),
    [
        dash.dependencies.Input("increase-date-button", "n_clicks"),
        dash.dependencies.Input("decrease-date-button", "n_clicks"),
        dash.dependencies.Input("duration-selector", "value"),
    ],
    [dash.dependencies.State("start-date-picker", "date")],
)
def update_date(increase_clicks, decrease_clicks, duration, current_date):
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]["prop_id"].split(".")[0]

    if duration == "Daily":
        days = 1
    else:
        days = 7

    if triggered_input == "increase-date-button":
        return (
            datetime.strptime(current_date, "%Y-%m-%d") + timedelta(days=days)
        ).strftime("%Y-%m-%d")
    elif triggered_input == "decrease-date-button":
        return (
            datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=days)
        ).strftime("%Y-%m-%d")
    else:
        return current_date


@app.callback(
    Output("duid-dropdown", "options"),
    Output("station-dropdown", "options"),
    Input("tech-type-dropdown", "value"),
    Input("dispatch-type-selector", "value"),
    Input("start-date-picker", "date"),
    Input("start-hour-picker", "value"),
    Input("start-minute-picker", "value"),
    Input("duration-selector", "value"),
    Input("region-checklist", "value"),
    State("duid-dropdown", "options"),
    State("station-dropdown", "options"),
)
def update_duid_station_options(
    tech_types: List[str],
    dispatch_type: str,
    start_date: str,
    hour: str,
    minute: str,
    duration: str,
    regions: List[str],
    initial_duid_options: List[str],
    initial_station_options: List[str],
) -> Tuple[List[str], str]:
    """
    Update the possible duid and station options based on the time period,
    duration and unit type.

    Arguments:
        tech_types: List of unit types
        dispatch_type: Either 'Generator' or 'Load'
        start_date: Date of initial datetime for graph in form 'DD-MM-YYYY',
            taken from the starting date picker.
        hour: Hour of initial datetime (in 24 hour format)
        minute: Minute of initial datetime
        duration: Defines the length of time to show data from. Either 'Daily'
            or 'Weekly'
        regions: List of regions to show data for
    Returns:
        duid options: List of possible duids for the given filters
        station options: List of possible stations for the given filters
    """
    if start_date is None:
        return dash.no_update, dash.no_update
    start_date = f'{start_date.replace("-", "/")} {hour}:{minute}:00'
    if tech_types is None:
        tech_types = []
    duid_options = get_duid_station_options(
        start_date, regions, duration, tech_types, dispatch_type
    )
    new_duid_options = sorted(duid_options["DUID"])
    if new_duid_options == initial_duid_options:
        new_duid_options = dash.no_update
    new_station_options = sorted(list(set(duid_options["STATION NAME"])))
    if new_station_options == initial_station_options:
        new_station_options = dash.no_update
    return new_duid_options, new_station_options


@app.callback(
    Output("tech-type-dropdown", "options"),
    Output("tech-type-dropdown", "value"),
    Input("dispatch-type-selector", "value"),
    Input("region-checklist", "value"),
)
def update_unit_type_options(
    dispatch_type: str,
    regions: List[str],
) -> Tuple[List[str], List[str]]:
    """
    Update the possible duid and station options based on the time period,
    duration and unit type.

    Arguments:
        dispatch_type: Either 'Generator' or 'Load'
        regions: List of regions to show data for
    Returns:
        unit type options: List of possible duids for the given filters
        unit type selected: List of possible stations for the given filters
    """
    unit_type_options = unit_types(regions, dispatch_type)
    return sorted(unit_type_options["UNIT TYPE"]), None


@app.callback(
    Output("duid-dropdown", "value"),
    Output("station-dropdown", "value"),
    Input("duid-dropdown", "value"),
    Input("tech-type-dropdown", "value"),
    Input("dispatch-type-selector", "value"),
    Input("station-dropdown", "value"),
    State("start-date-picker", "date"),
    State("start-hour-picker", "value"),
    State("start-minute-picker", "value"),
    State("duration-selector", "value"),
    State("region-checklist", "value"),
)
def update_duids_from_station(
    duids: List[str],
    tech_types: List[str],
    dispatch_type: str,
    stations: List[str],
    start_date: str,
    hour: str,
    minute: str,
    duration: str,
    regions: List[str],
) -> Tuple[List[str], str]:
    """
    Callback to update the duid dropdown when a station name is selected and
    remove the value from the station dropdown when the duid options are
    changed.

    Arguments:
        tech_types: List of unit types
        dispatch_type: Either 'Generator' or 'Load'
        duids: List of DUIDs currently selected in the DUID dropdown
        station: The currently selected station name in the station dropdown
        start_date: Date of initial datetime
        hour: Hour of initial datetime (in 24 hour format)
        minute: Minute of initial datetime
        duration: Either 'Daily' or 'Weekly'
        regions: List of currently selected regions
    Returns:
        'duid-dropdown' value (list): List of currently selected DUIDs. If a
            station has been selected, this consists of the list of all DUIDs
            that fall under that station.
        'station-dropdown' value (str): Name of currently selected station. If
            the 'duid-dropdown' was the component that triggered the callback,
            this value is empty.
    """
    trigger_id = dash.callback_context.triggered_id
    if not trigger_id:
        return dash.no_update, dash.no_update

    if trigger_id in ["duid-dropdown", "station-dropdown"] and stations:
        start_date = f'{start_date.replace("-", "/")} {hour}:{minute}:00'
        if tech_types is None:
            tech_types = []
        duid_options = get_duid_station_options(
            start_date, regions, duration, tech_types, dispatch_type
        )
        duid_options = duid_options.loc[duid_options["STATION NAME"].isin(stations)]
        duid_options = sorted(duid_options["DUID"])

    if trigger_id == "duid-dropdown":
        if not stations:
            return dash.no_update, dash.no_update
        if duids and sorted(duids) != duid_options:
            return dash.no_update, None
        return dash.no_update, dash.no_update

    elif trigger_id == "station-dropdown":
        if not stations:
            return dash.no_update, dash.no_update
        return duid_options, dash.no_update

    else:
        return None, None


@app.callback(
    Output("graph", "figure"),
    Output("error-message", "children"),
    Input("start-date-picker", "date"),
    Input("start-hour-picker", "value"),
    Input("start-minute-picker", "value"),
    Input("duration-selector", "value"),
    Input("region-checklist", "value"),
    Input("duid-dropdown", "value"),
    Input("price-demand-checkbox", "value"),
    Input("raw-adjusted-selector", "value"),
    Input("tech-type-dropdown", "value"),
    Input("dispatch-type-selector", "value"),
    Input("dispatch-checklist", "value"),
    Input("colour-dropdown", "value"),
    State("graph", "figure"),
)
def update_main_plot(
    start_date: str,
    hour: str,
    minute: str,
    duration: str,
    regions: List[str],
    duids: List[str],
    price_demand_checkbox: str,
    raw_adjusted: str,
    tech_types: List[str],
    dispatch_type: str,
    dispatch_metrics: List[str],
    color_scheme: str,
    fig: Figure,
) -> Tuple[Figure, str]:
    """
    Callback to update the graph when the user interacts with any of the graph
    selectors.

    Arguments:
        start_date: Date of initial datetime for graph in form 'DD-MM-YYYY',
            taken from the starting date picker.
        hour: Hour of initial datetime (in 24 hour format)
        minute: Minute of initial datetime
        duration: Defines the length of time to show data from. Either 'Daily'
            or 'Weekly'
        regions: List of regions to show data for
        duids: List of DUIDs of units to show data for
        price_demand_checkbox: Contains values 'Demand' and/or 'Price',
            controlling which of these measures is display
        raw_adjusted: Determines whether to show raw or availability adjusted
            bids. Either 'raw' or 'adjusted'
        tech_types: List of unit types to show bidding data for
        dispatch_type: Either 'Generator' or 'Load'
        dispatch_metrics: List of dispatch metrics to plot on main graph
        color_scheme: Name of the color scheme to use.
        fig: The current graph figure. If main filters remain the same, this
            figure is updated by adding or hiding traces, reducing loading time
    Returns:
        px figure showing the data specified using the graph selectors. See
            create_plots.plot_bids for more info.
        graph_name: The name of the graph being displayed
        error message: message shown if graph does not have the required
            data to be displayed
    """

    if start_date is None:
        return (
            dash.no_update,
            "Invalid date format, should be DD/MM/YY.",
        )

    start_date = f'{start_date.replace("-", "/")} {hour}:{minute}:00'
    start_date_obj = datetime.strptime(start_date, "%Y/%m/%d %H:%M:%S")
    if duration == "Daily":
        end_date = (start_date_obj + timedelta(days=1)).strftime("%Y/%m/%d %H:%M:%S")
        resolution = "5-min"
    elif duration == "Weekly":
        end_date = (start_date_obj + timedelta(days=7)).strftime("%Y/%m/%d %H:%M:%S")
        resolution = "hourly"

    # All of this is checking whether the graph can be updated quickly (i.e. by
    # adding or hiding traces) rather than redoing the entire thing. Should be
    # possible to do with the price plot too but alas I didn't have time to
    # figure it out
    fig = go.Figure(fig)
    trigger = dash.callback_context.triggered_id
    if trigger == "price-demand-checkbox":
        trace_names = [trace["name"] for trace in fig["data"]]

        if "Demand" in trace_names and "Demand" not in price_demand_checkbox:
            fig.update_traces(visible=False, selector={"name": "Demand"})
            update_colorbar_length(fig)
            return fig, ""
        if "Demand" in price_demand_checkbox:
            if "Demand" not in trace_names:
                fig = add_demand_trace(fig, start_date, end_date, regions)
            else:
                fig.update_traces(visible=True, selector={"name": "Demand"})
        if (
            "Demand on secondary plot" not in price_demand_checkbox
            and "Demand on secondary plot" in trace_names
        ):
            fig.update_traces(
                visible=False, selector={"name": "Demand on secondary plot"}
            )
            update_colorbar_length(fig)
            return fig, ""
        if (
            "Demand on secondary plot" in price_demand_checkbox
            and "Price" in trace_names
            and "Demand on secondary plot" in trace_names
        ):
            fig.update_traces(
                visible=True, selector={"name": "Demand on secondary plot"}
            )
        if (
            "Price" in trace_names
            and "Price" in price_demand_checkbox
            and "Demand on secondary plot" in trace_names
            and "Demand on secondary plot" in price_demand_checkbox
        ) or (
            "Price" not in trace_names
            and "Price" not in price_demand_checkbox
            and "Demand on secondary plot" not in trace_names
            and "Demand on secondary plot" not in price_demand_checkbox
        ):
            update_colorbar_length(fig)
            return fig, ""
    if trigger == "dispatch-checklist":
        trace_names = [trace["name"] for trace in fig["data"]]
        dispatch_options = DISPATCH_COLUMNS.keys()
        for name in trace_names:
            if name in dispatch_options and name not in dispatch_metrics:
                fig.update_traces(visible=False, selector={"name": name})
        for name in dispatch_metrics:
            if name not in trace_names:
                if duids:
                    fig = add_duid_dispatch_data(
                        fig, duids, start_date, end_date, resolution, [name]
                    )
                else:
                    fig = add_region_dispatch_data(
                        fig,
                        regions,
                        start_date,
                        end_date,
                        resolution,
                        dispatch_type,
                        tech_types,
                        [name],
                    )
            else:
                fig.update_traces(visible=True, selector={"name": name})
        update_colorbar_length(fig)
        return fig, ""

    show_demand = "Demand" in price_demand_checkbox
    show_demand_lower = "Demand on secondary plot" in price_demand_checkbox
    show_price = "Price" in price_demand_checkbox
    raw_adjusted = "raw" if raw_adjusted == "Raw Bids" else "adjusted"
    fig = plot_bids(
        start_date,
        end_date,
        resolution,
        regions,
        duids,
        show_demand,
        show_demand_lower,
        show_price,
        raw_adjusted,
        tech_types,
        dispatch_type,
        dispatch_metrics,
        color_scheme,
    )
    if not fig:
        return dash.no_update, "No data found using current filters"
    fig = adjust_fig_layout(fig)
    update_colorbar_length(fig)

    return fig, ""


@app.callback(
    Output("info", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("info", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


if __name__ == "__main__":
    application.run(debug=True, port=8080)
