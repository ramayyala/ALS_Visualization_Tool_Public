from modules.custom_groupings import custom_groupings_widgets
import ipyveutify as v
import pandas as pd
import panel as pn
from bokeh.models.widgets.tables import (CheckboxEditor, NumberEditor,
                                         SelectEditor)
from modules.local_databases import _local_databases
from modules.default import general_widgets
from modules.config import material
from modules import utils

def update_ccgm_group_widgets(*args):
    num_groups_str = custom_groupings_widgets.ccgm_num_groups.v_model
    if not num_groups_str:
        num_groups = 0
    else:
        num_groups = int(num_groups_str)
    if num_groups <= 1:

        # Clear existing widgets and update layout to remove group widgets
        pn.state.notifications.error(
            "Custom grouping requires at least 2 subgroups. Please enter a value of 2 or more in the Number of Groups field.",
            duration=3000,
        )
        custom_groupings_widgets.group_name_widgets.clear()
        custom_groupings_widgets.group_input_widgets.clear()
        custom_groupings_widgets.ccgm_layout.children = [
            v.Col(children=[custom_groupings_widgets.ccgm_custom_group_guide]),
            v.Col(
                children=[
                    custom_groupings_widgets.ccgm_grouping_name,
                    custom_groupings_widgets.ccgm_num_groups,
                ]
            ),
            v.Col(children=[custom_groupings_widgets.ccgm_close_modal_btn]),
        ]
        return
    # clear existing widgets before creating new ones
    custom_groupings_widgets.group_name_widgets.clear()
    custom_groupings_widgets.group_input_widgets.clear()
    # Create group name and input widgets dynamically
    for i in range(1, num_groups + 1):
        group_name = v.TextField(
            v_model="",
            placeholder=f"Please input the name of Group {i} here",
            style="width: 500px",
            label=f"Group {i} Name",
            outlined=True,
        )
        group_input = v.Textarea(
            style_="width: 650px",
            v_model="",
            placeholder=f"Please input your Group {i} Participant IDs here",
            label=f"Group {i} Participants",
            clearable=True,
            counter=True,
            outlined=True,
        )
        custom_groupings_widgets.group_name_widgets.append(group_name)
        custom_groupings_widgets.group_input_widgets.append(group_input)

    # Create cards for each group
    group_cards = []
    for name_widget, input_widget in zip(
        custom_groupings_widgets.group_name_widgets,
        custom_groupings_widgets.group_input_widgets,
    ):
        card = v.Card(
            children=[name_widget, input_widget],
            outlined=True,
            style_="width: 650px",
        )
        group_cards.append(card)

    # Arrange cards into rows with two cards per row
    group_rows = []
    for i in range(0, len(group_cards), 2):
        row = v.Row(
            children=[
                v.Col(children=[group_cards[i]]),
                (
                    v.Col(children=[group_cards[i + 1]])
                    if i + 1 < len(group_cards)
                    else v.Col()
                ),
            ]
        )
        group_rows.append(row)

    # Update custom_groupings_widgets.ccgm_layout
    custom_groupings_widgets.ccgm_layout.children = [
        v.Col(children=[custom_groupings_widgets.ccgm_custom_group_guide]),
        v.Col(
            children=[
                custom_groupings_widgets.ccgm_grouping_name,
                custom_groupings_widgets.ccgm_num_groups,
            ]
        ),
        *group_rows,
        v.Col(children=[custom_groupings_widgets.ccgm_close_modal_btn]),
    ]


# Callback that will open the modal when the button is clicked
def open_ccgm_callback(widget, event, data):
    material.modal[0].clear()
    material.modal[0].append(custom_groupings_widgets.ccgm_layout)
    material.open_modal()
    print("CCGM Modal Opened")


def open_ecgm_callback(widget, event, data):
    # ecgm_dropdown.items = covariates_dict.get("Custom")
    bokeh_editors = {
        "float": NumberEditor(),
        "bool": CheckboxEditor(),
        "str": SelectEditor(),
    }
    table_widget = pn.widgets.Tabulator(
        custom_groupings_df, selectable=True, editors=bokeh_editors
    )
    ecgm_layout = pn.Column(
        v.Card(
            outlined=True,
            elevated=True,
            children=[custom_groupings_widgets.ecgm_custom_group_guide],
        ),
        pn.Row(table_widget),
        v.Row(children=[custom_groupings_widgets.ecgm_close_modal_btn]),
    )
    material.modal[0].clear()
    material.modal[0].append(ecgm_layout)
    material.open_modal()
    print("ECGM Modal Opened")


def close_ccgm_callback(widget, event, data):
    participants = []
    group_values = []
    for name_widget, input_widget in zip(
        custom_groupings_widgets.group_name_widgets,
        custom_groupings_widgets.group_input_widgets,
    ):
        group_name = name_widget.v_model
        group_participants = input_widget.v_model.strip().split("\n")
        participants.extend(group_participants)
        group_values.extend([group_name] * len(group_participants))

    grouping_info = pd.DataFrame(
        {
            "Participant_ID": participants,
            custom_groupings_widgets.ccgm_grouping_name.v_model: group_values,
        }
    )
    global custom_groupings_df
    custom_groupings_df = pd.concat(
        [_local_databases.custom_groupings_df, grouping_info], ignore_index=True
    )
    # Update your covariates_dict and selectors accordingly
    # print(custom_groupings_df)
    # print("new custom grouping made")
    _local_databases.covariates_dict["Custom"].append(
        custom_groupings_widgets.ccgm_grouping_name.v_model
    )
    # print(covariates_dict)
    general_widgets.covariate_selector.items = _local_databases.covariates_dict.get(
        "Predefined"
    ) + _local_databases.covariates_dict.get("Custom")
    general_widgets.pca_covariate_selector.items = _local_databases.covariates_dict.get(
        "PCA_Predefined"
    ) + _local_databases.covariates_dict.get("Custom")
    general_widgets.multicovariate_selector.items = (
        _local_databases.covariates_dict.get("PCA_Predefined")
        + _local_databases.covariates_dict.get("Custom")
    )
    print(_local_databases.covariates_dict.get("Custom"))
    # covariates_dict["Custom"].append(custom_groupings_widgets.ccgm_grouping_name.v_model)
    # Update selectors here

    pn.state.notifications.success("Custom group successfully added", duration=1000)
    material.close_modal()


def close_ecgm_callback(widget, event, data):
    custom_groupings_widgets.ecgm_close_modal_btn.on_event("click", utils._update_plot)
    material.close_modal()


# Link the button to the callback and append it to the sidebar
# custom_groupings_widgets.ccgm_num_groups.on_event("input", update_ccgm_group_widgets)
# Observe changes in custom_groupings_widgets.ccgm_num_groups.v_model
custom_groupings_widgets.ccgm_num_groups.observe(update_ccgm_group_widgets, "v_model")

# Call the function initially to set up the widgets
update_ccgm_group_widgets()


custom_groupings_widgets.ccgm_open_modal_btn.on_event("click", open_ccgm_callback)
custom_groupings_widgets.ccgm_close_modal_btn.on_event("click", close_ccgm_callback)
custom_groupings_widgets.ecgm_open_modal_btn.on_event("click", open_ecgm_callback)
custom_groupings_widgets.ecgm_close_modal_btn.on_event("click", close_ecgm_callback)
