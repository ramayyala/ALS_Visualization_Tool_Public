import numpy as np
import pandas as pd
import plotly.express as px
from modules.default import general_widgets
from modules.sql import _sql
def dotplot():  # start function\
    from modules.utils import normalize, covariate_checker

    if general_widgets.dataset_button.v_model == "Transcriptomics":
        df_selected = _sql.tpm_sql_query(general_widgets.user_input.v_model, general_widgets.participant_input.v_model)
        index = "gene_id"
    elif general_widgets.dataset_button.v_model == "Proteomics":
        df_selected = _sql.protein_sql_query(general_widgets.user_input.v_model, general_widgets.participant_input.v_model)
        index = "Protein_ID"
    df_selected = normalize(general_widgets.norm_selector.v_model, df_selected)
    df_selected = df_selected.reset_index()
    df_selected = df_selected.melt(id_vars=index)
    df_selected.rename(
        columns={
            "variable": "Participant_ID",
            "value": "TPM",
        },
        inplace=True,
    )
    if general_widgets.covariate_selector.v_model == "None":
        fig = px.scatter(df_selected, x="TPM", y=index, width=1000, height=1000, hover_data=["Participant_ID"])
    else:
        df_selected = covariate_checker(df_selected, "Predefined")
        fig = px.scatter(
            df_selected,
            x="TPM",
            y=index,
            color=general_widgets.covariate_selector.v_model,
            width=1000,
            height=1000,
            hover_data=["Participant_ID"],
        )
    return fig



