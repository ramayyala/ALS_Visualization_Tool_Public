from modules.libraries import pn, v
## Custom Grouping Widgets


# Initialize the lists to hold group name and input widgets
group_name_widgets = []
group_input_widgets = []


ccgm_grouping_name = v.TextField(
    v_model="",
    placeholder="Please Input the name of your custom Grouping here",
    style="width: 500px",
    label="Grouping Name",
    outlined=True,
)

ccgm_num_groups = v.TextField(
    v_model=2,
    placeholder="Please input the number of subgroups in your custom grouping here",
    style="width: 500px",
    label="Number of Groups",
    outlined=True,
)

ccgm_custom_group_guide = v.Card(
    children=[
        v.CardText(
            class_="font-weight-bold",
            children=["1. Create a name for your custom grouping"],
        ),
        v.CardSubtitle(
            children=[
                "This is the name that will be stored and used for selecting your custom grouping later"
            ]
        ),
        v.CardText(class_="font-weight-bold", children=["2. Define your group names"]),
        v.CardSubtitle(
            children=[
                "This is the names of each of the subgroups in your custom grouping. These will appear as the values or the subclasses for your groupings"
            ]
        ),
        v.CardText(
            class_="font-weight-bold",
            children=["3. Input your participants tthat belong to each subgroup"],
        ),
        v.CardSubtitle(
            children=[
                "Input a list of participants, seperated by a new line for each participant, into each group that they belong to"
            ]
        ),
        v.CardText(class_="font-weight-bold", children=["4. Click submit"]),
        v.CardSubtitle(
            children=[
                "Once you click the submit button, the new custom grouping will be available at the bottom of the covariates menu"
            ]
        ),
    ]
)


ccgm_close_modal_btn = v.Btn(
    style_="background-color: #204CAC;", class_="white--text", children=["Submit"]
)


ccgm_layout = v.Card(
    children=[
        v.Col(children=[ccgm_custom_group_guide]),
        v.Col(children=[ccgm_grouping_name, ccgm_num_groups]),
        v.Col(children=[ccgm_close_modal_btn]),
    ]
)

# Create a button
ccgm_open_modal_btn = v.Btn(
    class_="white--text",
    outlined=True,
    style_="background-color: #204CAC; width:200px;",
    children=["Create Grouping"],
)


## EDIT CUSTOM GROUPINGS MODAL (ECGM)

ecgm_custom_group_guide = v.Card(
    children=[
        v.CardText(
            class_="font-weight-bold",
            children=["1. Edit the data"],
        ),
        v.CardSubtitle(
            children=[
                "This is a live editable dataframe widget of the custom groupings that have been created. To edit any of the data, just click into the cell you wish to edit. Once edited, the new edits are auto saved into the dataframe and will be reflected in the groupings on the plots"
            ]
        ),
        v.CardText(class_="font-weight-bold", children=["2. Advance Selection"]),
        v.CardSubtitle(
            children=[
                "Select rows on click. To select multiple use Ctrl-select. To select a range, use Shift-select."
            ]
        ),
        v.CardText(
            class_="font-weight-bold",
            children=["3. Click the Save Button"],
        ),
        v.CardSubtitle(
            children=[
                "This will save the edits made to the custom grouping to the system and auto update the plot if custom group is selected in the covariates widget."
            ]
        ),
    ]
)
ecgm_open_modal_btn = v.Btn(
    class_="white--text",
    outlined=True,
    style_="background-color: #204CAC; width:200px",
    children=["Edit Grouping"],
)

ecgm_close_modal_btn = v.Btn(
    style_="background-color: #204CAC;", class_="white--text", children=["Save"]
)



