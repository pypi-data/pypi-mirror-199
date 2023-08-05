"""Climeon plotting utilities."""

# Standard modules
import math

# External modules
from pandas import DataFrame
from plotly.graph_objects import Scatter
from plotly.subplots import make_subplots

STATES = [
    "INIT",
    "IDLE",
    "READY",
    "START",
    "RUNNING",
    "STOP",
    "MANUAL",
    "",
    "NOT_AVAILABLE",
    "TIMEOUT"
]

START_STATES = [
    "INIT",
    "AWAIT_COLD_WATER",
    "START_DT",
    "START_MAIN_PUMP",
    "AWAIT_HOT_WATER",
    "PHT_FLUSH_COOLING",
    "PHT_HEAT_UP_GAS",
    "PHT_HEAT_UP_COILS",
    "PHT_HEAT_UP_TURBINE",
    "PHT_DEC_BOOSTER",
    "COND_BEAR",
    "START_TURBINE",
    "PRE_COND_TURBINE",
    "AWAIT_TURBINE_SPEED",
    "START_BOOSTER_PUMP",
    "RAMP_UP_TURBINE",
    "AWAIT_START_SPEED"
]

STATUS_WORD = [
    "READY",
    "IDLE",
    "STARTING",
    "RUNNING",
    "STOPPING",
    "PLANNED_STOP",
    "UNPLANNED_STOP",
    "TIMEOUT",
    "LIMPMODE",
    "", # VACANT
    "", # VACANT
    "", # ALARM
    "", # CRITICAL_ALARM
    "", # EMERGENCY_ALARM
    "", # WARNING
    "", # VACANT
    "TURBINE_RUN",
    "MAIN_PUMP_RUN",
    "BOOSTER_PUMP_RUN",
    "BOOSTER_VALVE_OPEN",
    "COOLING_VALVE_OPEN",
    "", # VACANT
    "ATU_EVACUATING",
    "", # VACANT
    "", # DRAIN_VALVE_OPEN
    "", # SPRAY_VALVE_OPEN
    "", # GAS_VALVE_OPEN
    "", # EXHAUST_VALVE_OPEN
    "", # VACANT
    "", # VACANT
    "", # VACANT
    "REMOTE_CONTROL"
]

REGULATORS = [
    "",
    "Power regulator",
    "Current regulator",
    "Turbine winding temp",
    "Condenser pressure regulator",
    "Return water regulator",
    "Base regualtor",
    "Incomplete evap killer",
]

def add_transition(fig, data, variable, color, states, template, pos):
    """Add status transitions for a specific variable in a plotly figure."""
    # pylint: disable=too-many-arguments
    if variable not in data:
        return
    template = template or "%s"
    edges = data[(data[variable].diff() != 0).fillna(False)]
    for idx, (timestamp, state) in enumerate(zip(edges.index, edges[variable])):
        if idx == 0 or state == 0:
            continue
        if variable in ["StatusWord [-]", "SecondaryStatusWord [-]"]:
            bit = int(state ^ edges[variable][idx-1]).bit_length() - 1
            if not (state >> bit) & 1 or not states[bit]:
                continue
            text = "%s" % states[bit]
        elif states and not states[state]:
            continue
        elif states:
            text = template % states[state]
        elif "%s" in template:
            text = template % state
        else:
            text = template
        fig.add_vline(x=timestamp, line_width=1, line_dash="dash", line_color=color)
        fig.add_annotation(x=timestamp, y=pos, text=text, yref="paper")

def add_transitions(fig, data):
    """Add all possible state transitions.

    Parameters:
        fig (figure):       A plotly figure.
        data (DataFrame):   A pandas dataframe with data.
    """
    # pylint: disable=too-many-arguments
    add_transition(fig, data, "State [-]", "blue", STATES, None, 0.96)
    #add_transition(fig, data, "StartState [-]", "green", START_STATES, None, 0.96)
    add_transition(fig, data, "AlarmCode [-]", "red", None, "AlarmCode %s", 1.04)
    add_transition(fig, data, "NoOfGreasingCyclesFrontBearing [-]", "blue",
                   None, "Front greasing", 1)
    add_transition(fig, data, "NoOfGreasingCyclesRearBearing [-]", "blue",
                   None, "Rear greasing", 1)
    add_transition(fig, data, "NoOfAtuCycles [-]", "green", None, "ATU", 1)
    if "State [-]" not in data:
        add_transition(fig, data, "StatusWord [-]", "green", STATUS_WORD, None, 0.96)
    if "Wetgas detected [-]" in data:
        color_code(fig, data["Wetgas detected [-]"], [None, "red"])
    elif "SecondaryStatusWord [-]" in data:
        wet_gas = (data["SecondaryStatusWord [-]"] & (1 << 10) > 0) * 1
        color_code(fig, wet_gas, [None, "red"])

def color_code(fig, state, colors, text=""):
    """Color code the background of a plot based on state."""
    state_notnull = state.fillna(False)
    state_changes = state_notnull[state_notnull.diff() != 0]
    for idx, timestamp in enumerate(state_changes.index):
        if idx == len(state_changes) - 1:
            end_idx = state.index[-1]
        else:
            end_idx = state_changes.index[idx + 1]
        color = colors[int(state_changes[timestamp])]
        if color is not None:
            fig.add_vrect(timestamp, end_idx, annotation_text=text,
                          fillcolor=color, opacity=0.2, line_width=0)

def add_regulators(fig, data):
    """Add active regulator to a plot."""
    temp = data.copy()
    temp["ActiveController [-]"] = \
        (data["SecondaryStatusWord [-]"].apply(lambda x: (x >> 24) & 1) * 1) + \
        (data["SecondaryStatusWord [-]"].apply(lambda x: (x >> 25) & 1) * 2) + \
        (data["SecondaryStatusWord [-]"].apply(lambda x: (x >> 26) & 1) * 3) + \
        (data["SecondaryStatusWord [-]"].apply(lambda x: (x >> 27) & 1) * 4) + \
        (data["SecondaryStatusWord [-]"].apply(lambda x: (x >> 28) & 1) * 5) + \
        (data["SecondaryStatusWord [-]"].apply(lambda x: (x >> 29) & 1) * 6) + \
        (data["SecondaryStatusWord [-]"].apply(lambda x: (x >> 30) & 1) * 7)
    add_transition(fig, temp, "ActiveController [-]", "green", REGULATORS, None, 1)

def standard_plot(data):
    """Create a plot with state transitions and useful variables."""
    # pylint: disable=too-many-statements
    specs = [[{"secondary_y": True}], [{"secondary_y": True}]]
    fig = make_subplots(2, 1, shared_xaxes=True, vertical_spacing=0.02, specs=specs)
    fig.update_layout(hovermode="x", height=900)
    fig.update_traces(mode="lines", hovertemplate=None)

    # 1st plot: Power and Control with state transitions
    # 1st axis [kW], [krpm]
    add_trace(fig, data, "PowerOutput [kW]", 1)
    if "TurbSpeed [rpm]" in data:
        data["TurbSpeed [krpm]"] = data["TurbSpeed [rpm]"] / 1000
        add_trace(fig, data, "TurbSpeed [krpm]", 1)

    # 2nd axis [%]
    add_trace(fig, data, "AV25Pos [%]", 1, secondary_y=True)
    add_trace(fig, data, "AV26Pos [%]", 1, secondary_y=True)
    add_trace(fig, data, "Fcp91Speed [%]", 1, secondary_y=True)
    add_trace(fig, data, "Fcp92Speed [%]", 1, secondary_y=True)

    # 2nd plot: Variables galore
    # 1st axis [deg C]

    # Hot side
    add_trace(fig, data, "T38 [deg C]", 2, visible="legendonly")
    add_trace(fig, data, "T39 [deg C]", 2, visible="legendonly")
    data["HX DT [deg C]"] = data["T38 [deg C]"] - data["T39 [deg C]"]
    add_trace(fig, data, "HX DT [deg C]", 2, visible="legendonly")
    if "T42 [deg C]" in data:
        lower_gas = data["T33 [deg C]"].fillna(data["T42 [deg C]"])
        upper_gas = data["T51 [deg C]"].fillna(data["T54 [deg C]"])
        data["Gas [deg C]"] = DataFrame([lower_gas, upper_gas]).min()
    else:
        data["Gas [deg C]"] = data["T33 [deg C]"]
    if "HxCalcBoilingPoint [deg C]" in data:
        boil = data["HxCalcBoilingPoint [deg C]"]
    else:
        boil = 1219.97 / (7.1327 - (data["P74 [bar]"] / 0.00133322).apply(math.log10)) - 230.653
    data["SuperHeat [deg C]"] = data["Gas [deg C]"] - boil
    data["DT Gas [deg C]"] = data["T38 [deg C]"] - data["Gas [deg C]"]
    add_trace(fig, data, "Gas [deg C]", 2, visible="legendonly")
    add_trace(fig, data, "SuperHeat [deg C]", 2, visible="legendonly")
    add_trace(fig, data, "DT Gas [deg C]", 2, visible="legendonly")

    # Cold side
    add_trace(fig, data, "T36 [deg C]", 2, visible="legendonly")
    add_trace(fig, data, "T37 [deg C]", 2, visible="legendonly")
    data["CX DT [deg C]"] = data["T37 [deg C]"] - data["T36 [deg C]"]
    data["Pinch [deg C]"] = data["T35 [deg C]"] - data["T36 [deg C]"]
    add_trace(fig, data, "CX DT [deg C]", 2, visible="legendonly")
    add_trace(fig, data, "Pinch [deg C]", 2, visible="legendonly")

    # Turbine
    if "T43 [deg C]" in data:
        data["Coil [deg C]"] = data[["T43 [deg C]", "T44 [deg C]", "T45 [deg C]"]].max(axis=1)
        add_trace(fig, data, "Coil [deg C]", 2, visible="legendonly")
    add_trace(fig, data, "T46 [deg C]", 2, visible="legendonly")
    add_trace(fig, data, "T47 [deg C]", 2, visible="legendonly")

    # 2nd axis [bar], [-]
    data["TurbPressDiff [bar]"] = data["P74 [bar]"] - data["P71 [bar]"]
    data["TurbPressRatio [-]"] = data["P74 [bar]"] / data["P71 [bar]"]
    data["Cushion [bar]"] = data["Cushion [mbar]"] / 1000
    if "P81 [bar]" in data:
        data["CX DP water [bar]"] = data["P79 [bar]"] - data["P81 [bar]"]
    data["CX DP media [bar]"] = data["P101 [bar]"] - data["P77 [bar]"]
    data["FCP91 DP [bar]"] = data["P101 [bar]"] - data["P72 [bar]"]
    data["Condenser DP [bar]"] = data["P77 [bar]"] - data["P71 [bar]"]
    add_trace(fig, data, "TurbPressDiff [bar]", 2, visible="legendonly", secondary_y=True)
    add_trace(fig, data, "TurbPressRatio [-]", 2, visible="legendonly", secondary_y=True)
    add_trace(fig, data, "Cushion [bar]", 2, visible="legendonly", secondary_y=True)
    add_trace(fig, data, "P71 [bar]", 2, visible="legendonly", secondary_y=True)
    add_trace(fig, data, "CX DP water [bar]", 2, visible="legendonly", secondary_y=True)
    add_trace(fig, data, "CX DP media [bar]", 2, visible="legendonly", secondary_y=True)
    add_trace(fig, data, "FCP91 DP [bar]", 2, visible="legendonly", secondary_y=True)
    add_trace(fig, data, "Condenser DP [bar]", 2, visible="legendonly", secondary_y=True)

    fig["layout"]["yaxis"]["title"] = "[kW], [krpm]"
    fig["layout"]["yaxis2"]["title"] = "[%]"
    fig["layout"]["yaxis2"]["showgrid"] = False
    fig["layout"]["yaxis2"]["zeroline"] = False
    fig["layout"]["yaxis3"]["title"] = "[deg C]"
    fig["layout"]["yaxis4"]["title"] = "[bar], [-]"
    fig["layout"]["yaxis4"]["showgrid"] = False
    fig["layout"]["yaxis4"]["zeroline"] = False

    add_transitions(fig, data)
    return fig

def add_trace(fig, data, variable, row, visible=None, yaxis=None, secondary_y=False):
    """Add a trace to a figure."""
    # pylint: disable=too-many-arguments
    if not variable in data:
        return
    trace = Scatter(x=data.index, y=data[variable].values, name=variable,
                    visible=visible, yaxis=yaxis)
    fig.add_trace(trace, row=row, col=1, secondary_y=secondary_y)
