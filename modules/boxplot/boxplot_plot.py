import numpy as np
import pandas as pd
import plotly.express as px
from modules.default import general_widgets
from modules.local_databases import _local_databases
from modules.sql import _sql
from modules import utils

def boxplot():  # start function
    if general_widgets.dataset_button.v_model == "Transcriptomics":
        df_selected = _sql.tpm_sql_query(
            general_widgets.user_input.v_model,
            general_widgets.participant_input.v_model,
        )
        index = "gene_id"
    elif general_widgets.dataset_button.v_model == "Proteomics":
        df_selected = _sql.protein_sql_query(
            general_widgets.user_input.v_model,
            general_widgets.participant_input.v_model,
        )
        index = "Protein_ID"
    df_selected = utils.normalize(general_widgets.norm_selector.v_model, df_selected)
    df_selected = df_selected.reset_index()
    df_selected = df_selected.melt(id_vars=index)
    df_selected.rename(
        columns={"variable": "Participant_ID", "value": "TPM"}, inplace=True
    )
    if general_widgets.covariate_selector.v_model == "None":
        print(general_widgets.stripplot_switch.v_model)
        if general_widgets.stripplot_switch.v_model:
            fig = px.box(
                df_selected,
                x=index,
                y="TPM",
                width=1000,
                height=1000,
                hover_data=["Participant_ID"],
            )
            strip_fig = px.strip(
                df_selected,
                x=index,
                y="TPM",
                stripmode="group",
                hover_data=["Participant_ID"],
            )
            for trace in strip_fig.data:
                fig.add_trace(trace)
        else:
            fig = px.box(
                df_selected,
                x=index,
                y="TPM",
                width=1000,
                height=1000,
                hover_data=["Participant_ID"],
            )
        # fig.add_trace(go.Scatter(x=df_selected.index, y=df_selected["TPM"]))
    else:

        df_selected = utils.covariate_checker(df_selected, "Predefined")
        if general_widgets.stripplot_switch.v_model:
            fig = px.box(
                df_selected,
                x=index,
                y="TPM",
                color=general_widgets.covariate_selector.v_model,
                width=1000,
                height=1000,
                hover_data=["Participant_ID"],
            )
            strip_fig = px.strip(
                df_selected,
                x=index,
                y="TPM",
                color=general_widgets.covariate_selector.v_model,
                stripmode="group",
                hover_data=["Participant_ID"],
            )
            for trace in strip_fig.data:
                fig.add_trace(trace)
        else:
            print(df_selected)
            fig = px.box(
                df_selected,
                x=index,
                y="TPM",
                color=general_widgets.covariate_selector.v_model,
                width=1000,
                height=1000,
                hover_data=["Participant_ID"],
            )

    return fig
