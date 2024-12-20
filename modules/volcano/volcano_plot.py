import numpy as np
import pandas as pd
import plotly.express as px
from modules.default import general_widgets
from modules.sql import _sql


def volcano_plot():  # start function
    if general_widgets.dataset_button.v_model == "Transcriptomics":
        df_selected = _sql.de_sql_query(general_widgets.user_input.v_model)
        index = "gene_id"
    elif general_widgets.dataset_button.v_model == "Proteomics":
        df_selected = _sql.protein_de_sql_query(general_widgets.user_input.v_model)
        index = "Protein_ID"
    df_selected.loc[
        df_selected["log2FoldChange"] > general_widgets.log2FC_input.v_model, "group"
    ] = "NotSignificant"
    df_selected.loc[
        (df_selected["padj"] < general_widgets.p_value_input.v_model)
        & (
            np.absolute(df_selected["log2FoldChange"])
            < general_widgets.log2FC_input.v_model
        ),
        "group",
    ] = "Significant"
    df_selected.loc[
        (df_selected["padj"] > general_widgets.p_value_input.v_model)
        & (
            np.absolute(df_selected["log2FoldChange"])
            > general_widgets.log2FC_input.v_model
        ),
        "group",
    ] = "FoldChange"
    df_selected.loc[
        (df_selected["padj"] < general_widgets.p_value_input.v_model)
        & (
            np.absolute(df_selected["log2FoldChange"])
            > general_widgets.log2FC_input.v_model
        ),
        "group",
    ] = "Significant&FoldChange"
    fig = px.scatter(
        df_selected,
        x="log2FoldChange",
        y="negative_log_pval",
        color="group",
        labels={
            "log2FoldChange": "Log2FoldChange",
            "negative_log_pval": "-1og10 P-value",
        },
        hover_data=[index],
        width=1250,
        height=1000,
    )
    return fig
