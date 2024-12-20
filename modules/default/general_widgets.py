from modules.libraries import v
from modules.local_databases import _local_databases

# Feedback Button
feedback_btn = v.Container(
    style_="background-color: #204CAC; width: 220px",
    children=[
        v.Btn(
            style_="background-color: white; width: 200px",
            children=["Send Feedback"],
            rounded=True,
            href="https://forms.gle/DnSN4cvhxGVAmfDy7",
        )
    ],
)


# Changelog Button
changelog_btn = v.Container(
    style_="background-color: #204CAC; width: 220px",
    children=[
        v.Btn(
            style_="background-color: white; width: 200px",
            rounded=True,
            children=["What's New!"],
        )
    ],
)

# Dataset changer widget
dataset_button = v.Select(
    style_="width: 400px",
    outlined=True,
    label="Select Dataset",
    items=["Transcriptomics", "Proteomics"],
    v_model="Transcriptomics",
)

# Graph Choice wdiget
graph_button = v.Select(
    style_="width: 400px",
    outlined=True,
    label="Select Plot",
    items=_local_databases._data_choices[dataset_button.v_model],
    v_model="Boxplot",
)

user_dropdown = v.Select(
    style_="width: 400px",
    outlined=True,
    label="Select Pathway",
    items=_local_databases._user_dropdown_options[dataset_button.v_model],
    v_model=_local_databases._user_dropdown_options[dataset_button.v_model][0],
)
user_input = v.Textarea(
    style_="width: 400px",
    v_model=_local_databases._user_input[dataset_button.v_model][user_dropdown.v_model][
        0
    ],
    label="Gene ID Input",
    clearable=True,
    clear_icon="mdi-close-circle-outline",
    outlined=True,
)


# Participant List
participant_input = v.Textarea(
    style_="width: 400px",
    v_model="",
    label="Participant List",
    clearable=True,
    clear_icon="mdi-close-circle-outline",
    persistent_clear=False,
    outlined=True,
    center_affix=False,
)

# Covariate Selector
multicovariate_selector = v.Select(
    style_="width: 400px",
    outlined=True,
    label="Select Covariate",
    items=_local_databases.covariates_dict.get("PCA_Predefined"),
    multiple=True,
    chips=True,
    v_model=["Sex", "Race"],
)
covariate_selector = v.Select(
    style_="width: 400px",
    outlined=True,
    label="Select Covariate",
    items=_local_databases.covariates_dict.get("Predefined"),
    v_model="None",
    chips=True,
)
pca_covariate_selector = v.Select(
    style_="width: 400px",
    outlined=True,
    label="Select Covaraite",
    items=_local_databases.covariates_dict.get("PCA_Predefined"),
    v_model="Sex",
    chips=True,
)


# log2fc and p-value inputs

p_value_input = v.Slider(max=1, min=0, step=0.01, v_model=0.05, label="Select P-Value")
p_value_counter = v.TextField(v_model=0.05)

log2FC_input = v.Slider(
    max=5, min=-5, step=0.05, v_model=1.5, label="Select log2FC Value"
)
log2FC_counter = v.TextField(v_model=1.5)

# Color Pickers
positive_col = v.ColorPicker(
    mode="hexa", v_model="#0657E9", title="Select Positive Color"
)
negative_col = v.ColorPicker(
    mode="hexa", v_model="#165805", title="Select Negative Color"
)

quick_start_guide = v.Card(
    children=[
        v.CardText(class_="font-weight-bold", children=["1. Select Dataset"]),
        v.CardSubtitle(
            children=[
                "Enables users to select their preferred dataset for visualization purposes."
            ]
        ),
        v.CardSubtitle(
            class_="font-weight-bold",
            children=["Note:Proteomics Dataset is batch corrected."],
        ),
        v.CardText(class_="font-weight-bold", children=["2. Select Plot"]),
        v.CardSubtitle(
            children=[
                "Allows users to choose which type of visualization they wish to use"
            ]
        ),
        v.CardText(class_="font-weight-bold", children=["3. Select Pathway"]),
        v.CardSubtitle(
            children=[
                "Enables users to select the preferred type of visualization they intend to use"
            ]
        ),
        v.CardText(class_="font-weight-bold", children=["4. Participant List"]),
        v.CardSubtitle(
            children=[
                "Enables users to choose from a list of KEGG Pathways. Upon Selecting a pathway, a corresponding set of Gene/UniProt IDS will be automatically chosen for visualization. These gnee idtentifers will be displayed in the Gene ID/UniProtKB ID Input Widget below."
            ]
        ),
    ]
)

# strip plot widget for adding strip plot to box plot
stripplot_switch = v.Switch(label="Enable Strip Plot", v_model=False)


# Normalization Options
norm_selector = v.Select(
    style_="width: 400px",
    outlined=True,
    label="",
    items=["None", "Log Norm", "Z-Score", "Quantile Norm"],
    v_model="Log Norm",
    chips=True,
)
