from functools import partial

import numpy as np
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
from modules import utils
from modules.clustermap import clustermap_widgets
from modules.default import general_widgets
from modules.local_databases import _local_databases
from plotly.subplots import make_subplots
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist
from modules.sql import _sql


# helper function for sorting traces in clustermap function
def sort_traces(rdt, cdt):
    """Sort row dendrogram clusters and column dendrogram clusters
       so that the background trace (above threshold) is trace 0
    and all other traces are ordered top-to-bottom (row dendrogram)
    or left-to-right (column dendrogram).

    Parameters:
    - rdt (list[dict]): The row dendrogram cluster traces.
    - cdt (list[dict]): The column dendrogram cluster traces.

    Returns:
    - tuple: The sorted row dendrogram clusters and column
        dendrogram clusters.
    """

    tmp_rdt = []
    tmp_cdt = []

    if len(rdt) > 0:
        # first, find background trace: (max 'x')
        rdt.sort(key=lambda t: -1 * max(list(t["x"])))
        tmp_rdt.append(rdt[0])
        # then, sort top-to-bottom
        r = rdt[1:]
        r.sort(key=lambda t: -1 * min(list(t["y"])))
        tmp_rdt += r
    if len(cdt) > 0:
        # background trace has max 'y'
        cdt.sort(key=lambda t: -1 * max(list(t["y"])))
        tmp_cdt.append(cdt[0])
        # sort left to right
        c = cdt[1:]
        c.sort(key=lambda t: min(list(t["x"])))
        tmp_cdt += c

    return (tmp_rdt, tmp_cdt)


def clustermap():  # start function
    if general_widgets.dataset_button.v_model == "Transcriptomics":
        df_selected = _sql.tpm_sql_query(
            general_widgets.user_input.v_model,
            general_widgets.participant_input.v_model,
        )
    elif general_widgets.dataset_button.v_model == "Proteomics":
        df_selected = _sql.protein_sql_query(
            general_widgets.user_input.v_model,
            general_widgets.participant_input.v_model,
        )
    # print("test2")
    print(general_widgets.multicovariate_selector.v_model)
    if any(
        item in general_widgets.multicovariate_selector.v_model
        for item in _local_databases.covariates_dict.get("Custom")
    ):
        custom_cov = [
            item
            for item in general_widgets.multicovariate_selector.v_model
            if item in _local_databases.covariates_dict.get("Custom")
        ]
        custom_cov.append("Participant_ID")
        predef_cov = [
            item
            for item in general_widgets.multicovariate_selector.v_model
            if item not in _local_databases.covariates_dict.get("Custom")
        ]
        print(predef_cov)
        if (
            not predef_cov
        ):  # no predefined covariate is selected, meanign only custom grouping selected in covariates
            covariates = _local_databases.custom_groupings_df[custom_cov]
            covariates = covariates.set_index("Participant_ID")

        else:  # predef_cov is not empty, meaning there is mix of custom and predefined covariates
            predef_cov = _sql.cov_sql_query(predef_cov)
            custom_cov = _local_databases.custom_groupings_df[custom_cov]
            covariates = pd.merge(predef_cov, custom_cov, on="Participant_ID")
            covariates = covariates.set_index("Participant_ID")
            print(covariates)
    else:
        covariates = _sql.cov_sql_query(general_widgets.multicovariate_selector.v_model)
        print(covariates)
    df_selected = utils.normalize(general_widgets.norm_selector.v_model, df_selected)
    # set up participant and gene id lists
    gene_ids = df_selected.index.values
    participants = df_selected.columns.values
    # convert df_selected into an array for input
    array_selected = df_selected.to_numpy()
    # define covariate list
    covariate_list = general_widgets.multicovariate_selector.v_model

    # Initialize trace_list
    trace_list = {"col": [], "row": []}

    # Step 1: Create dendrograims
    # NOTE: CHANGE metric and method input to be dependent on user input for distance and linkage function
    pw_euclid_func = partial(pdist, metric=clustermap_widgets.distance_selector.v_model)
    linkage_func = partial(linkage, method=clustermap_widgets.linkage_selector.v_model)

    cols_dendro = ff.create_dendrogram(
        array_selected.T,
        orientation="bottom",
        labels=participants,
        distfun=pw_euclid_func,
        linkagefun=linkage_func,
    )
    rows_dendro = ff.create_dendrogram(
        array_selected,
        orientation="right",
        labels=gene_ids,
        distfun=pw_euclid_func,
        linkagefun=linkage_func,
    )
    trace_list["col"] = cols_dendro.data
    trace_list["row"] = rows_dendro.data

    # Reorder data array
    clustered_column_ids = cols_dendro["layout"]["xaxis"]["ticktext"]
    clustered_row_ids = rows_dendro["layout"]["yaxis"]["ticktext"]
    df_reordered = df_selected.reindex(
        index=clustered_row_ids, columns=clustered_column_ids
    ).astype(float)
    array_selected = df_reordered.to_numpy()

    # Initialize plot
    fig = make_subplots(
        rows=5,
        cols=5,
        specs=[
            [{}, {}, {"colspan": 2}, None, {}],
            [{}, {}, {"colspan": 2}, None, {}],
            [
                {"rowspan": 2},
                {"rowspan": 2},
                {"colspan": 2, "rowspan": 2},
                None,
                {"rowspan": 2},
            ],
            [None, None, None, None, None],
            [{}, {}, {"colspan": 2}, None, {}],
        ],
        vertical_spacing=0,
        horizontal_spacing=0,
    )
    fig.update_layout(hovermode="closest")

    # Process dendrogram traces and tick values
    tickvals_col, tickvals_row = [], []

    for dt_col in trace_list["col"]:
        xs, ys = np.array(dt_col["x"], dtype=float), np.array(dt_col["y"], dtype=float)
        dt_col.update(x=xs, y=ys)
        tickvals_col += [
            x for x, y in zip(xs.flatten(), ys.flatten()) if y == 0.0 and x % 10 == 5
        ]

    for dt_row in trace_list["row"]:
        xs, ys = np.array(dt_row["x"], dtype=float), np.array(dt_row["y"], dtype=float)
        dt_row.update(x=xs, y=ys)
        tickvals_row += [
            y for x, y in zip(xs.flatten(), ys.flatten()) if x == 0.0 and y % 10 == 5
        ]

    tickvals_col = sorted(set(tickvals_col))
    tickvals_row = sorted(set(tickvals_row))

    # Update axis settings
    for a in [
        "xaxis",
        "xaxis3",
        "xaxis5",
        "xaxis6",
        "xaxis7",
        "xaxis9",
        "xaxis10",
        "xaxis11",
        "yaxis1",
        "yaxis3",
        "yaxis5",
        "yaxis6",
        "yaxis7",
        "yaxis9",
        "yaxis10",
        "yaxis11",
    ]:
        fig["layout"][a].update(
            type="linear",
            showline=False,
            showgrid=False,
            zeroline=False,
            mirror=False,
            fixedrange=False,
            showticklabels=False,
        )

    # Sort traces
    row_dendro_traces, col_dendro_traces = sort_traces(
        list(trace_list["row"]), list(trace_list["col"])
    )

    # Add dendrogram traces to the figure
    for i, cdt in enumerate(col_dendro_traces):
        cdt.update(name=f"Col Cluster {i}", hoverinfo="y+name")
        fig.add_trace(cdt, 1, 3)

    for i, rdt in enumerate(row_dendro_traces):
        rdt.update(name=f"Row Cluster {i}", hoverinfo="x+name")
        fig.add_trace(rdt, 3, 1)

    # Align dendrograms and heatmap
    yaxis9 = fig["layout"]["yaxis9"]
    yaxis9.update(scaleanchor="y11")
    xaxis3 = fig["layout"]["xaxis3"]
    xaxis3.update(scaleanchor="x11")

    tickvals_col = tickvals_col or [
        10 * i + 5 for i in range(len(clustered_column_ids))
    ]
    tickvals_row = tickvals_row or [10 * i + 5 for i in range(len(clustered_row_ids))]

    # Update axis settings for labels
    fig["layout"]["xaxis11"].update(
        tickmode="array",
        tickvals=tickvals_col,
        ticktext=clustered_column_ids,
        showticklabels=True,
        side="bottom",
        showline=False,
        range=[min(tickvals_col) - 5, max(tickvals_col) + 5],
    )
    fig["layout"]["yaxis11"].update(
        tickmode="array",
        tickvals=tickvals_row,
        ticktext=clustered_row_ids,
        showticklabels=True,
        side="right",
        showline=False,
    )
    colorscale = [
        [0, general_widgets.negative_col.v_model[:7]],
        [1, general_widgets.positive_col.v_model[:7]],
    ]
    # Create heatmap
    heatmap = go.Heatmap(
        x=tickvals_col,
        y=tickvals_row,
        z=array_selected,
        colorscale=colorscale,
        colorbar={"xpad": 100},
        hovertemplate="Participant_ID: %{x}<br>Gene_ID: %{y}<br>Value: %{z}<br>",
    )
    fig.add_trace(heatmap, 3, 3)

    # Step 5: Add covariate column on x-axis of heatmap
    next_enum_value = 1
    enum_dict = {}
    for covariate in covariate_list:
        unique_values = covariates[covariate].unique()
        enum_dict[covariate] = {
            value: idx + next_enum_value for idx, value in enumerate(unique_values)
        }
        next_enum_value += len(unique_values)

    cov_reordered = covariates.apply(
        lambda x: x.map(enum_dict[x.name]) if x.name in enum_dict else x
    )

    cov_reordered = cov_reordered.reindex(index=clustered_column_ids)
    # Generate enum_matrix with consistent dimensions
    enum_matrix = []
    customdata_matrix = []

    for covariate in covariate_list:
        cov_values = (
            cov_reordered[covariate].values if covariate in cov_reordered else np.nan
        )
        enum_matrix.append(cov_values)

        # Create customdata for hovertemplate
        cov_customdata = (
            covariates[covariate].reindex(index=clustered_column_ids).values
            if covariate in covariates
            else np.nan
        )
        customdata_matrix.append(cov_customdata)

    enum_matrix = np.array(enum_matrix)
    customdata = np.dstack(
        (
            np.tile(cov_reordered.index.values, (len(covariate_list), 1)),
            np.array(customdata_matrix),
        )
    )

    # Generate covariate heatmap
    cov_heatmap = go.Heatmap(
        x=tickvals_col,
        y=tickvals_row,
        z=enum_matrix,
        colorscale="Viridis",
        coloraxis="coloraxis",
        customdata=customdata,
        hovertemplate="Participant_ID: %{customdata[0]}<br>Covariate: %{y}<br>%{y}: %{customdata[1]}<br>",
    )
    fig.add_trace(cov_heatmap, 2, 3)
    cov_tickvals = [10 * (i + 1) for i in range(len(covariate_list))]
    # Finalize layout
    fig.update_layout(
        xaxis7={"matches": "x11"},
        coloraxis_showscale=False,
        yaxis7=dict(
            tickmode="array",
            tickvals=cov_tickvals,
            ticktext=covariate_list,
            showticklabels=True,
        ),
        yaxis9={"range": [min(tickvals_row), max(tickvals_row)]},
        showlegend=False,
        hovermode="closest",
        width=1000,
        height=1000,
    )

    # Adjust domain for proper alignment
    row_ratio = 0.95 / (1 + int(1 / 0.2)) if row_dendro_traces else 0
    col_ratio = 0.95 / (1 + int(1 / 0.2)) if col_dendro_traces else 0

    fig["layout"]["xaxis1"].update(domain=[0, 0.95])
    fig["layout"]["xaxis3"].update(domain=[row_ratio, 0.95], anchor="y9")
    fig["layout"]["xaxis5"].update(domain=[0, 0.95])
    fig["layout"]["xaxis7"].update(domain=[row_ratio, 0.95], anchor="y9")
    fig["layout"]["xaxis9"].update(domain=[0, row_ratio])
    fig["layout"]["xaxis10"].update(domain=[row_ratio, row_ratio])
    fig["layout"]["xaxis11"].update(domain=[row_ratio, 0.95])
    return fig
