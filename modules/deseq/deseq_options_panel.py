from modules.custom_groupings import custom_groupings_widgets
from modules.default import general_widgets
from modules.deseq import deseq_widgets
from modules.libraries import v

deseq_options_panel = v.ExpansionPanels(
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
                        general_widgets.user_dropdown,
                        general_widgets.user_input,
                        general_widgets.participant_input,
                        general_widgets.covariate_selector,
                        deseq_widgets.deseq_run_btn,
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
