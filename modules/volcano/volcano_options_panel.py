import ipyvuetify as v
from modules.default import general_widgets

volcano_options_panel = v.ExpansionPanels(
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
                        v.Container(
                            children=[
                                general_widgets.p_value_input,
                                general_widgets.p_value_counter,
                            ]
                        ),
                        v.Container(
                            children=[
                                general_widgets.log2FC_input,
                                general_widgets.log2FC_counter,
                            ]
                        ),
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
                v.ExpansionPanelContent(children=["Coming Soon"]),
            ]
        ),
    ],
)
