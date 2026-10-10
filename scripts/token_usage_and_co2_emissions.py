# Copied from the development repository (climate_intelligence/plots/
# token_usage_and_co2_emissions.py), which is the source of truth. Re-copy when
# it changes. Invoked by scripts/build_footprint.py with explicit paths.
"""Created by JXP and Claude.

Bokeh plots of Claude's token usage and estimated CO2 emissions over time,
built from the logging summary table (``Logs/log_summary.csv``). The output is a
standalone HTML file intended to eventually be exposed on the Climate
Intelligence blog (GitHub Pages).

Layout (per the Discussion in Logs/logging.md, prompt 5):
  1. PRIMARY (large) panel: cumulative CO2 emissions — the headline number —
     with the granular per-prompt/daily CO2 on a secondary axis.
  2. Secondary panel: tokens used over time, points coloured by model.
  3. A "Per prompt / Daily" toggle switches the granular series between
     one-point-per-prompt and daily aggregates. The toggle is pure CustomJS,
     so it works in static HTML with no Bokeh server.

Run directly to (re)generate the HTML::

    python climate_intelligence/plots/token_usage_and_co2_emissions.py

Optional arguments let you point at a different CSV or output path; see ``main``.
"""

# Imports at the top of the file (project coding guideline).
import argparse
from pathlib import Path

import pandas as pd

from bokeh.plotting import figure, save, output_file
from bokeh.models import (ColumnDataSource, HoverTool, LinearAxis, Range1d,
                          RadioButtonGroup, CustomJS)
from bokeh.layouts import column
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap

# Repo-relative defaults: this file lives at climate_intelligence/plots/,
# so the repository root is two directories up. The HTML lands in Logs/
# alongside the data it visualizes (logging.md, prompt 6).
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = REPO_ROOT / "Logs" / "log_summary.csv"
DEFAULT_HTML = REPO_ROOT / "Logs" / "token_usage_and_co2_emissions.html"

# CO2-to-car-miles conversion (logging.md, prompt 7): 0.36 kg (~0.8 lb) of CO2
# per mile driven. Stored in grams to match the log's units.
GRAMS_CO2_PER_MILE = 360.0


def load_usage_log(csv_path):
    """Created by JXP and Claude.

    Load and prepare the logging summary table for plotting.

    Inputs
    ------
    csv_path : str or pathlib.Path
        Path to ``log_summary.csv`` with columns ``ut_time``, ``tokens_used``,
        ``model``, ``co2_grams_estimate``.

    Outputs
    -------
    pandas.DataFrame
        The log sorted by time, with ``ut_time`` parsed to timezone-naive UTC
        datetimes and a ``cumulative_co2`` column (running sum of the CO2
        estimate, in grams) added.
    """
    # Parse the ISO-8601 UT timestamps; pandas handles the trailing 'Z'.
    df = pd.read_csv(csv_path)
    df["ut_time"] = pd.to_datetime(df["ut_time"], utc=True).dt.tz_localize(None)

    # Sort chronologically so lines and the cumulative sum are meaningful.
    df = df.sort_values("ut_time").reset_index(drop=True)

    # Running total of emissions — the headline number for a climate blog.
    df["cumulative_co2"] = df["co2_grams_estimate"].cumsum()

    # Same total expressed as car-miles driven, for an intuitive scale
    # (logging.md, prompt 7). Used in the hover and the twin miles axis.
    df["cumulative_miles"] = df["cumulative_co2"] / GRAMS_CO2_PER_MILE
    return df


def aggregate_daily(df):
    """Created by JXP and Claude.

    Aggregate the per-prompt log to daily totals for the toggle view.

    Inputs
    ------
    df : pandas.DataFrame
        Prepared log table from :func:`load_usage_log`.

    Outputs
    -------
    (pandas.DataFrame, pandas.DataFrame)
        ``daily_tokens``: one row per (UTC day, model) with summed tokens, so
        the colour-by-model mapping survives aggregation.
        ``daily_co2``: one row per UTC day with summed CO2. Both use noon UT of
        the day as the plotting timestamp.
    """
    day = df["ut_time"].dt.floor("D")

    # Tokens: keep the model split so daily points stay colour-coded.
    daily_tokens = (
        df.assign(day=day)
          .groupby(["day", "model"], as_index=False)["tokens_used"].sum()
    )
    daily_tokens["ut_time"] = daily_tokens["day"] + pd.Timedelta(hours=12)

    # CO2: total emissions per day (model split matters less for the headline).
    daily_co2 = (
        df.assign(day=day)
          .groupby("day", as_index=False)["co2_grams_estimate"].sum()
    )
    daily_co2["ut_time"] = daily_co2["day"] + pd.Timedelta(hours=12)
    return daily_tokens, daily_co2


def make_co2_figure(source, daily_co2_source, df):
    """Created by JXP and Claude.

    Create the PRIMARY panel: cumulative CO2, with granular CO2 secondary.

    Inputs
    ------
    source : bokeh.models.ColumnDataSource
        Per-prompt data source (ut_time, co2_grams_estimate, cumulative_co2, ...).
    daily_co2_source : bokeh.models.ColumnDataSource
        Daily-aggregate CO2 source (ut_time, co2_grams_estimate).
    df : pandas.DataFrame
        Prepared log table; used to scale the secondary axis.

    Outputs
    -------
    (bokeh.plotting.figure, list, list)
        The figure, the per-prompt renderers, and the daily renderers (the two
        renderer lists are wired to the view toggle).
    """
    # Cumulative CO2 is the headline, so it owns the LEFT axis and the height.
    fig = figure(
        title="Estimated cumulative CO2 emissions — with car-miles equivalent (0.36 kg CO2/mile)",
        x_axis_type="datetime",
        height=420,
        sizing_mode="stretch_width",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        y_axis_label="Cumulative CO2 (g)",
    )

    # Pin the cumulative (left) axis to the data extent with headroom. A fixed
    # range lets the twin "miles" axis stay a true proportional mirror; the
    # CustomJS link below keeps them locked under any pan/zoom too.
    max_cum = float(df["cumulative_co2"].max()) if len(df) else 1.0
    fig.y_range = Range1d(start=0, end=max_cum * 1.1)

    # Twin LEFT axis: the same cumulative total read as miles driven by a car
    # (grams / 360). No glyphs are drawn on it — it is purely an alternate ruler
    # for the headline line, so a reader sees both "grams" and "miles" at once.
    fig.extra_y_ranges = {
        "miles": Range1d(start=0, end=max_cum * 1.1 / GRAMS_CO2_PER_MILE),
    }
    fig.add_layout(
        LinearAxis(y_range_name="miles",
                   axis_label="≈ equivalent miles driven by a car (cumulative)"),
        "left",
    )
    # Keep the miles ruler locked to the CO2 axis under pan/zoom (static-HTML safe).
    _link = CustomJS(args=dict(miles=fig.extra_y_ranges["miles"],
                               f=GRAMS_CO2_PER_MILE),
                     code="miles.start = cb_obj.start / f; "
                          "miles.end = cb_obj.end / f;")
    fig.y_range.js_on_change("start", _link)
    fig.y_range.js_on_change("end", _link)

    # Primary series: the running total, always visible in both views.
    cumulative = fig.line("ut_time", "cumulative_co2", source=source,
                          line_width=3, color="#d62728", legend_label="cumulative CO2")

    # Secondary axis for granular (per-prompt or daily) emissions.
    max_granular = float(max(
        df["co2_grams_estimate"].max(),
        daily_co2_source.data["co2_grams_estimate"].max() if
        len(daily_co2_source.data["co2_grams_estimate"]) else 0.0,
    )) if len(df) else 1.0
    # Add (do not replace) the granular range so the "miles" twin axis set up
    # above survives.
    fig.extra_y_ranges["granular"] = Range1d(start=0, end=max_granular * 1.1)
    fig.add_layout(LinearAxis(y_range_name="granular", axis_label="CO2 per prompt / day (g)"),
                   "right")

    # Per-prompt view (visible by default).
    per_prompt = fig.scatter("ut_time", "co2_grams_estimate", source=source,
                             y_range_name="granular", size=9, color="#2ca02c",
                             alpha=0.85, legend_label="per prompt")

    # Daily-aggregate view (hidden until toggled).
    daily = fig.scatter("ut_time", "co2_grams_estimate", source=daily_co2_source,
                        y_range_name="granular", size=13, marker="diamond",
                        color="#2ca02c", alpha=0.9, visible=False)

    # Hover on the cumulative line plus each granular series.
    fig.add_tools(HoverTool(
        renderers=[per_prompt],
        tooltips=[("time (UT)", "@ut_time{%F %T}"),
                  ("CO2 (g)", "@co2_grams_estimate{0,0.00}"),
                  ("cumulative (g)", "@cumulative_co2{0,0.00}"),
                  ("≈ miles driven", "@cumulative_miles{0,0.0}"),
                  ("model", "@model")],
        formatters={"@ut_time": "datetime"},
    ))
    fig.add_tools(HoverTool(
        renderers=[daily],
        tooltips=[("day", "@ut_time{%F}"),
                  ("CO2 (g/day)", "@co2_grams_estimate{0,0.00}")],
        formatters={"@ut_time": "datetime"},
    ))
    fig.add_tools(HoverTool(
        renderers=[cumulative],
        tooltips=[("time (UT)", "@ut_time{%F %T}"),
                  ("cumulative (g)", "@cumulative_co2{0,0.00}"),
                  ("≈ miles driven", "@cumulative_miles{0,0.0}")],
        formatters={"@ut_time": "datetime"},
    ))
    fig.legend.location = "top_left"
    return fig, [per_prompt], [daily]


def make_token_usage_figure(source, daily_tokens_source, models):
    """Created by JXP and Claude.

    Create the secondary panel: token usage over time, coloured by model.

    Inputs
    ------
    source : bokeh.models.ColumnDataSource
        Per-prompt data source.
    daily_tokens_source : bokeh.models.ColumnDataSource
        Daily (day, model) aggregated token source.
    models : list of str
        Distinct model names, used to colour points categorically.

    Outputs
    -------
    (bokeh.plotting.figure, list, list)
        The figure, per-prompt renderers, and daily renderers for the toggle.
    """
    fig = figure(
        title="Token usage over time",
        x_axis_type="datetime",
        height=280,
        sizing_mode="stretch_width",
        tools="pan,wheel_zoom,box_zoom,reset,save",
        y_axis_label="Tokens",
    )

    # Shared colour mapping: same palette in both views, keyed by model name.
    # Category10 needs at least 3 entries; guard the small-N case.
    palette = Category10[max(3, len(models))][: max(1, len(models))]
    color = factor_cmap("model", palette=palette, factors=models)

    # Per-prompt view (visible by default): trend line + points.
    trend = fig.line("ut_time", "tokens_used", source=source,
                     line_width=1, color="gray", alpha=0.5)
    per_prompt = fig.scatter("ut_time", "tokens_used", source=source,
                             size=10, color=color, alpha=0.85, legend_field="model")

    # Daily-aggregate view (hidden until toggled): one diamond per (day, model).
    daily = fig.scatter("ut_time", "tokens_used", source=daily_tokens_source,
                        size=14, marker="diamond", color=color, alpha=0.9,
                        visible=False)

    fig.add_tools(HoverTool(
        renderers=[per_prompt],
        tooltips=[("time (UT)", "@ut_time{%F %T}"),
                  ("tokens", "@tokens_used{0,0}"),
                  ("model", "@model")],
        formatters={"@ut_time": "datetime"},
    ))
    fig.add_tools(HoverTool(
        renderers=[daily],
        tooltips=[("day", "@ut_time{%F}"),
                  ("tokens/day", "@tokens_used{0,0}"),
                  ("model", "@model")],
        formatters={"@ut_time": "datetime"},
    ))
    fig.legend.location = "top_left"
    fig.legend.title = "model"
    return fig, [trend, per_prompt], [daily]


def make_view_toggle(per_prompt_renderers, daily_renderers):
    """Created by JXP and Claude.

    Build the "Per prompt / Daily" toggle that flips renderer visibility.

    Inputs
    ------
    per_prompt_renderers : list
        Renderers shown in the per-prompt view (all panels).
    daily_renderers : list
        Renderers shown in the daily-aggregate view (all panels).

    Outputs
    -------
    bokeh.models.RadioButtonGroup
        Widget with a CustomJS callback — works in static HTML (no server),
        which is what GitHub Pages will need.
    """
    toggle = RadioButtonGroup(labels=["Per prompt", "Daily"], active=0)
    toggle.js_on_change("active", CustomJS(
        args=dict(per=per_prompt_renderers, daily=daily_renderers),
        code="""
        const show_daily = cb_obj.active == 1;
        for (const r of per)   { r.visible = !show_daily; }
        for (const r of daily) { r.visible = show_daily; }
        """,
    ))
    return toggle


def build_dashboard(csv_path=DEFAULT_CSV, output_html=DEFAULT_HTML):
    """Created by JXP and Claude.

    Assemble the toggle and both panels into a single HTML file.

    Inputs
    ------
    csv_path : str or pathlib.Path
        Path to the logging summary CSV. Defaults to ``Logs/log_summary.csv``.
    output_html : str or pathlib.Path
        Destination HTML file. Defaults to a file next to this script.

    Outputs
    -------
    pathlib.Path
        The path to the written HTML file.
    """
    df = load_usage_log(csv_path)
    daily_tokens, daily_co2 = aggregate_daily(df)

    # One source per series; the toggle only flips renderer visibility.
    source = ColumnDataSource(df)
    daily_tokens_source = ColumnDataSource(daily_tokens)
    daily_co2_source = ColumnDataSource(daily_co2)

    # Distinct models, as strings, for categorical colouring in both views.
    models = [str(m) for m in df["model"].astype(str).unique().tolist()]

    # Cumulative CO2 is the headline: build it first and put it on top, larger.
    co2_fig, co2_per, co2_daily = make_co2_figure(source, daily_co2_source, df)
    tok_fig, tok_per, tok_daily = make_token_usage_figure(source, daily_tokens_source, models)

    # Link the two time axes so panning/zooming one moves the other.
    tok_fig.x_range = co2_fig.x_range

    toggle = make_view_toggle(co2_per + tok_per, co2_daily + tok_daily)

    output_html = Path(output_html)
    output_html.parent.mkdir(parents=True, exist_ok=True)
    output_file(filename=str(output_html), title="Climate Intelligence — usage & CO2")
    save(column(toggle, co2_fig, tok_fig, sizing_mode="stretch_width"))
    return output_html


def main():
    """Created by JXP and Claude.

    Command-line entry point: regenerate the HTML dashboard.

    Inputs
    ------
    (command line) ``--csv`` path to the summary CSV, ``--out`` output HTML path.

    Outputs
    -------
    None. Writes an HTML file and prints its location.
    """
    parser = argparse.ArgumentParser(description="Plot token usage and CO2 emissions over time.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Path to log_summary.csv")
    parser.add_argument("--out", default=str(DEFAULT_HTML), help="Output HTML path")
    args = parser.parse_args()

    written = build_dashboard(args.csv, args.out)
    print(f"Wrote {written}")


if __name__ == "__main__":
    main()
