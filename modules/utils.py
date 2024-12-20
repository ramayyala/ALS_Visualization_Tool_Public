from modules.boxplot import boxplot_plot
from modules.clustermap import (clustermap_options_panel, clustermap_plot,
                                clustermap_widgets)
from modules.shared import material
from modules.default import general_widgets, options_panel
from modules.distplot import distplot_plot
from modules.dotplot import dotplot_plot
from modules.libraries import np, pd, pn
from modules.local_databases import _local_databases
from modules.pca import pca_options, pca_plot_2D
from modules.pca import pca_plot_3D
from modules.sql import _sql
from modules.violin import violin_plot
from modules.volcano import volcano_options_panel, volcano_plot
from scipy import stats


# Normalization Function
def normalize(norm_value, df_selected):
    if norm_value == "None":
        return df_selected
    elif norm_value == "Log Norm":
        df_selected = (1 + df_selected) / 2  # (-1,1] -> (0,1]
        df_selected = np.log(df_selected)
        return df_selected
    elif norm_value == "Z-Score":
        df_selected = stats.zscore(df_selected)
        return df_selected
    elif norm_value == "Quantile Norm":
        df_sorted = pd.DataFrame(
            np.sort(df_selected.values, axis=0),
            index=df_selected.index,
            columns=df_selected.columns,
        )
        df_mean = df_sorted.mean(axis=1)
        df_mean.index = np.arange(1, len(df_mean) + 1)
        df_selected = (
            df_selected.rank(method="min").stack().astype(int).map(df_mean).unstack()
        )
        return df_selected


def covariate_checker(df_selected, covariate_type):
    if covariate_type == "Predefined":
        if (
            general_widgets.covariate_selector.v_model
            in _local_databases.covariates_dict.get("Predefined")
        ):
            covariates = _sql.cov_sql_query(general_widgets.covariate_selector.v_model)
            df_selected = pd.merge(df_selected, covariates, on="Participant_ID")
        else:
            covariates = _local_databases.custom_groupings_df[
                ["Participant_ID", general_widgets.covariate_selector.v_model]
            ]
            df_selected = pd.merge(df_selected, covariates, on="Participant_ID")

    elif covariate_type == "PCA_Predefined":
        if (
            general_widgets.pca_covariate_selector.v_model
            in _local_databases.covariates_dict.get("PCA_Predefined")
        ):
            covariates = _sql.cov_sql_query(
                general_widgets.pca_covariate_selector.v_model
            )
            meta = covariates[[general_widgets.pca_covariate_selector.v_model]]
            df_selected = df_selected.merge(meta, left_index=True, right_index=True)
        else:  # general_widgets.pca_covariate_selector_choice is custom
            meta = _local_databases.custom_groupings_df[
                ["Participant_ID", general_widgets.pca_covariate_selector.v_model]
            ]
            df_selected = pd.merge(
                df_selected, meta, on="Participant_ID"
            )  # X=df_selected
            df_selected = df_selected.set_index("Participant_ID")
    return df_selected


# dotplot
# violin plot
def load_plot(graph_button, event, data):
    if graph_button.v_model == "Boxplot":
        material.main[0].objects = [
            pn.Row(boxplot_plot.boxplot, height=1000, visible=True)
        ]
        material.mainsidebar[0].objects = [pn.Column(options_panel.options_panel)]
    elif graph_button.v_model == "Clustermap":
        material.main[0].objects = [
            pn.Row(clustermap_plot.clustermap, height=1000, visible=True)
        ]
        material.mainsidebar[0].objects = [
            pn.Column(clustermap_options_panel.clustermap_options_panel)
        ]
    elif graph_button.v_model == "Volcano Plot":
        material.main[0].objects = [
            pn.Row(volcano_plot.volcano_plot, height=1000, visible=True)
        ]
        material.mainsidebar[0].objects = [
            pn.Column(volcano_options_panel.volcano_options_panel)
        ]
    elif graph_button.v_model == "PCA 2D Plot":
        material.main[0].objects = [
            pn.Row(pca_plot_2D.pca_plot_2d, height=1000, visible=True)
        ]
        material.mainsidebar[0].objects = [pn.Column(pca_options.pca_options_panel)]
    elif graph_button.v_model == "PCA 3D Plot":
        material.main[0].objects = [
            pn.Row(pca_plot_3D.pca_plot_3d, height=1000, visible=True)
        ]
        material.mainsidebar[0].objects = [pn.Column(pca_options.pca_options_panel)]
    # proteomics additions
    elif graph_button.v_model == "Dotplot":
        material.main[0].objects = [
            pn.Row(dotplot_plot.dotplot, height=1000, visible=True)
        ]
        material.mainsidebar[0].objects = [pn.Column(options_panel)]
    elif graph_button.v_model == "Violin Plot":
        material.main[0].objects = [
            pn.Row(violin_plot.violinplot, height=1000, visible=True)
        ]
        material.mainsidebar[0].objects = [pn.Column(options_panel)]
    elif graph_button.v_model == "Distribution Plot":
        material.main[0].objects = [
            pn.Row(distplot_plot.distplot, height=1000, visible=True)
        ]
        material.mainsidebar[0].objects = [pn.Column(options_panel)]
    else:
        print("graph selected is not available")


# graph_button.on_click(load_plot)
general_widgets.graph_button.on_event("change", load_plot)


def _update_local_participants():
    _local_databases._local_participant_list[general_widgets.dataset_button.v_model] = (
        general_widgets.participant_input.v_model
    )
    # print(participant_input.v_model)
    num_participants = str(
        len(
            str(
                _local_databases._local_participant_list.get(
                    general_widgets.dataset_button.v_model
                )
            ).split("\n")
        )
    )
    general_widgets.participant_input.label = (
        "Participant List (n=" + num_participants + ")"
    )
    print("update participant count")


def _update_plot(widget, event, data):
    print("plot update")
    _update_local_participants()
    if general_widgets.graph_button.v_model == "Boxplot":
        material.main[0].objects = [
            pn.Row(boxplot_plot.boxplot, height=1000, visible=True)
        ]
    elif general_widgets.graph_button.v_model == "Clustermap":
        material.main[0].objects = [
            pn.Row(clustermap_plot.clustermap, height=1000, visible=True)
        ]
    elif general_widgets.graph_button.v_model == "Volcano Plot":
        material.main[0].objects = [
            pn.Row(volcano_plot.volcano_plot, height=1000, visible=True)
        ]
    elif general_widgets.graph_button.v_model == "PCA 2D Plot":
        material.main[0].objects = [
            pn.Row(pca_plot_2D.pca_plot_2d, height=1000, visible=True)
        ]
    elif general_widgets.graph_button.v_model == "PCA 3D Plot":
        material.main[0].objects = [
            pn.Row(pca_plot_3D.pca_plot_3d, height=1000, visible=True)
        ]
    # proteomics additions
    elif general_widgets.graph_button.v_model == "Dotplot":
        material.main[0].objects = [
            pn.Row(dotplot_plot.dotplot, height=1000, visible=True)
        ]
    elif general_widgets.graph_button.v_model == "Violin Plot":
        material.main[0].objects = [
            pn.Row(violin_plot.violinplot, height=1000, visible=True)
        ]
    elif general_widgets.graph_button.v_model == "Distribution Plot":
        material.main[0].objects = [
            pn.Row(distplot_plot.distplot, height=1000, visible=True)
        ]
    else:
        print("edit does not exist")


def _update_gene_list(user_dropdown, event, data):
    print("select gene list")
    gene_list = _local_databases._user_input[general_widgets.dataset_button.v_model][
        general_widgets.user_dropdown.v_model
    ]
    general_widgets.user_input.v_model = gene_list[0]
    # user_input.label = "Gene ID Input (n=" + str(len(gene_list[0])) = ")"


def _update_p_value_counter(p_value_input, event, data):
    general_widgets.p_value_counter.v_model = p_value_input.v_model
    print("select pvalue")


def _update_log2FC_counter(log2FC_input, event, data):
    print("select log2FC value")
    general_widgets.log2FC_counter.v_model = log2FC_input.v_model


# update function for switching between datasets
def switch_data(dataset_button, event, data):
    if general_widgets.dataset_button.v_model == "Transcriptomics":
        index = _local_databases._user_dropdown_options["Transcriptomics"].index(
            general_widgets.user_dropdown.v_model
        )
        general_widgets.user_dropdown.v_model = _local_databases._user_dropdown_options[
            "Transcriptomics"
        ][index]
        general_widgets.user_dropdown.items = _local_databases._user_dropdown_options[
            "Transcriptomics"
        ]
        gene_list = _local_databases._user_input[
            general_widgets.dataset_button.v_model
        ][general_widgets.user_dropdown.v_model]
        general_widgets.user_input.v_model = gene_list[0]
        # _update_input(user_dropdown.v_model, event, data)
        general_widgets.user_input.label = "Gene ID Input"
        general_widgets.graph_button.items = _local_databases._data_choices[
            "Transcriptomics"
        ]
        if not _local_databases._local_participant_list["Transcriptomics"]:
            participants = list(
                set(
                    _local_databases._participant_list[
                        general_widgets.dataset_button.v_model
                    ][0].split("\n")
                ).intersection(
                    list(set(general_widgets.participant_input.v_model.split("\n")))
                )
            )
            general_widgets.participant_input.label = (
                "Participant List (n=" + str(len(participants)) + ")"
            )
            _local_databases._local_participant_list["Proteomics"] = (
                general_widgets.participant_input.v_model
            )
            general_widgets.participant_input.v_model = "\n".join(participants)
        else:
            _local_databases._local_participant_list["Proteomics"] = (
                general_widgets.participant_input.v_model
            )
            participants = _local_databases._local_participant_list.get(
                "Transcriptomics"
            )
            num_participants = str(
                len(
                    str(
                        _local_databases._local_participant_list.get("Transcriptomics")
                    ).split("\n")
                )
            )
            general_widgets.participant_input.v_model = participants
            general_widgets.participant_input.label = (
                "Participant List (n=" + num_participants + ")"
            )
        print("switch", general_widgets.dataset_button.v_model)
        pn.state.notifications.success(
            "Dataset Switched to Transcriptomics", duration=3000
        )
    elif general_widgets.dataset_button.v_model == "Proteomics":
        index = _local_databases._user_dropdown_options["Proteomics"].index(
            general_widgets.user_dropdown.v_model
        )
        general_widgets.user_dropdown.v_model = _local_databases._user_dropdown_options[
            "Proteomics"
        ][index]
        general_widgets.user_dropdown.items = _local_databases._user_dropdown_options[
            "Proteomics"
        ]
        gene_list = _local_databases._user_input[
            general_widgets.dataset_button.v_model
        ][general_widgets.user_dropdown.v_model]
        general_widgets.user_input.v_model = gene_list[0]
        # _update_input(user_dropdown.v_model, event, data)
        general_widgets.user_input.label = "UniProtKB ID Input"
        general_widgets.graph_button.items = _local_databases._data_choices[
            "Proteomics"
        ]
        if not _local_databases._local_participant_list["Proteomics"]:

            participants = list(
                set(
                    _local_databases._participant_list[
                        general_widgets.dataset_button.v_model
                    ][0].split("\n")
                ).intersection(
                    list(set(general_widgets.participant_input.v_model.split("\n")))
                )
            )

            general_widgets.participant_input.label = (
                "Participant List (n=" + str(len(participants)) + ")"
            )
            _local_databases._local_participant_list["Transcriptomics"] = (
                general_widgets.participant_input.v_model
            )

            general_widgets.participant_input.v_model = "\n".join(participants)
        else:
            _local_databases._local_participant_list["Transcriptomics"] = (
                general_widgets.participant_input.v_model
            )
            participants = _local_databases._local_participant_list.get("Proteomics")
            num_participants = str(
                len(
                    str(
                        _local_databases._local_participant_list.get("Proteomics")
                    ).split("\n")
                )
            )
            general_widgets.participant_input.v_model = participants
            general_widgets.participant_input.label = (
                "Participant List (n=" + num_participants + ")"
            )

        print("switch", general_widgets.dataset_button.v_model)
        pn.state.notifications.success("Dataset Switched to Proteomics", duration=3000)
    else:
        pn.state.notifications.error("Dataset does not exist", duration=3000)
        print("Dataset does not exist")


general_widgets.dataset_button.on_event("input", switch_data)
general_widgets.dataset_button.on_event("change", _update_plot)


general_widgets.p_value_input.on_event("input", _update_p_value_counter)
general_widgets.log2FC_input.on_event("input", _update_log2FC_counter)
general_widgets.p_value_input.on_event("change", _update_plot)
general_widgets.log2FC_input.on_event("change", _update_plot)
general_widgets.p_value_counter.on_event("change", _update_plot)
general_widgets.log2FC_counter.on_event("change", _update_plot)

general_widgets.user_dropdown.on_event("input", _update_gene_list)
general_widgets.user_dropdown.on_event("change", _update_plot)

general_widgets.user_input.on_event("input", _update_plot)
# participant_input.on_event("update:vModel", _update_local_participants)
general_widgets.participant_input.on_event("input", _update_plot)

general_widgets.positive_col.on_event("input", _update_plot)
general_widgets.negative_col.on_event("input", _update_plot)

general_widgets.multicovariate_selector.on_event("change", _update_plot)
general_widgets.covariate_selector.on_event("change", _update_plot)


general_widgets.pca_covariate_selector.on_event("change", _update_plot)
general_widgets.norm_selector.on_event("change", _update_plot)

clustermap_widgets.linkage_selector.on_event("change", _update_plot)
clustermap_widgets.distance_selector.on_event("change", _update_plot)

general_widgets.stripplot_switch.on_event("change", _update_plot)
