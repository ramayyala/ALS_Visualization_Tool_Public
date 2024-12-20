from modules.clustermap import clustermap_widgets
import ipyvuetify as v
from modules.custom_groupings import custom_groupings_widgets
from modules.default import general_widgets

clustermap_options_panel = v.ExpansionPanels(
    v_model=[0, 1],
    multiple=True,
    accordion=True,
    style_="padding-left: 1px; min-width: 200px",
    children=[
        v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(
                    class_="font-weight-bold", children=["Basic Options"]
                ),
                v.ExpansionPanelContent(
                    children=[
                        general_widgets.dataset_button,
                        general_widgets.graph_button,
                        general_widgets.user_dropdown,
                        general_widgets.user_input,
                        general_widgets.participant_input,
                        general_widgets.multicovariate_selector,
                        general_widgets.norm_selector,
                        clustermap_widgets.distance_selector,
                        clustermap_widgets.linkage_selector,
                        "Select Positive Color",
                        general_widgets.positive_col,
                        "Select Negative Color",
                        general_widgets.negative_col,
                    ]
                ),
            ]
        ),
        # Advanced Options Exapnsion Panel
        v.ExpansionPanel(
            children=[
                v.ExpansionPanelHeader(
                    class_="font-weight-bold", children=["Advanced Options"]
                ),
                v.ExpansionPanelContent(
                    children=[
                        v.Row(
                            children=[
                                custom_groupings_widgets.ccgm_open_modal_btn,
                                custom_groupings_widgets.ecgm_open_modal_btn,
                            ]
                        )
                    ]
                ),
            ]
        ),
    ],
)
