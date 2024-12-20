import numpy as np
import pandas as pd
import plotly.express as px
from modules.default import general_widgets
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from modules.sql import _sql

def pca_plot_2d():
    from modules.utils import covariate_checker
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
    df_selected = df_selected.T
    df_selected = df_selected.reset_index()
    df_selected = df_selected.rename(columns={"index": "Participant_ID"})
    df_selected = df_selected.set_index("Participant_ID")

    df_selected = covariate_checker(df_selected, "PCA_Predefined")
    # print(df_selected)
    X = df_selected.iloc[:, :-1]
    X = StandardScaler().fit_transform(X)
    pca = PCA(n_components=2)
    components = pca.fit_transform(X)
    fig = px.scatter(
        components,
        x=0,
        y=1,
        color=df_selected[general_widgets.pca_covariate_selector.v_model],
        width=1000,
        height=1000,
    )
    return fig


