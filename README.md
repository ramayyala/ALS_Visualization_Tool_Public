# ANSWER ALS VISUALIZATION TOOL

This is the github repository for the Answer ALS Visualization tool.
This repository contains all code, images, and references used for building the tool. All data is stored seperately on the SQL Server.
**NOTE**: The code in this repository is currently nonfunctional, as all relevant API keys and sensitive information have been removed. This repository is provided solely to showcase the code’s structure and approach.

## Table of Contents

- [**Dependencies**](./README.md#dependencies)
- [**Getting Started**](./README.md#getting-started)
- [**Widgets**](./README.md#widgets)
- [**Functions**](./README.md#functions)
- [**Visualizations**](./README.md#visualizations)
- [**Differential Expression Analysis Module**](./README.md#differential-expression-analysis-module)
- [**Custom Groupings Module**](./README.md#custom-groupings-module)

## Dependencies

This project is dependent on the couple of core dependencies. For best results with development, we refer you to our [Getting Started](./README.md#getting-started) Section. For the full list of dependecies, please check out the [requirements.txt](./requirements.txt) or the [als\_viz.yml](./als_viz.yml).

## Getting Started

In order to quickly set up your environment to develop for this tool, we have two methods for doing so. We reccommend the first method as it is by far the easiest for setting up your virtual environment. We reccomend the second method if you prefer not to you use conda/mamba, but you will need to use pip then. Regardless, of the method, we still reccommend setting up virtual environments for developmental purposes. Below, we will show you the first method.

### First Method: Quick Installation via Virtual Environment Importing&#x20;

**[Conda]("https://docs.conda.io/en/latest/" "conda")**\*\* Method:\*\*

`conda env create --file als_viz.yaml`

**[Mamba]("https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html" "conda")**\*\* Method:\*\*

`mamba env create --file als_viz.yaml`

This will auto-install all of the necessary packages needed for developing for this tool and running this tool in its current state.

### First Method: Installation via pip

**Conda Method:**

`conda create -n <environment_name>`

**Mamba Method:**

`mamba create -n <environment_name>`

Moving forward for this method, the guide will follow using mamba as our package manager, but the commands will be exactly the same bewteen using conda and mamba. Please look at mamba documentation or conda documentation if you have more questions.

Once you have created your environment, please active the environment so we can install the necessary dependencies as shown below:

`mamba activate <environment_name>`

You will know your evironment has changed because the (base) parameter on your terminal screen will change to the name of your environment you just activated.
Next we will install the new package manager we need to install the packages we need:

`mamba install pip`

From here, we will just install the packages using pip:

`pip install -r requirements.txt`

Finally once you have everything installed, you need to install the  ODBC Driver 17 for SQL Server provided by Microsoft. You need to make sure you have this installed prior to running as this is how SQL querying works. More details on the SQL querying of the data can be found in the [SQL Querying](./README.md#sql-querying) Section.

To test if everything runs correctly, we reccomend quickly running the following command:

`panel serve main.py`

It should open you to the local web-page version of the tool on the website. If you reach the tool page, then you have successfully installed the development environment.

## Widgets

For the widgets, there are two classes of widgets we use: Veutify and Panel based widgets.

### [Veutify Widgets](https://ipyvuetify.readthedocs.io/en/latest/ "Veutify")

#### **dataset\_button:**

This widget uses the v.Select() widget. It allows the user to switch between the datasets. It is also a widget that is linked to the graph\_button widget via the \_data\_choices dictionary. When a dataset is selected, it calls the plots that are available for that dataset from the \_data\_choices dictionary and loads those in as the available options to be selected in the graph\_button widget. For more details on the v.Select() widget please see the ipyvuetify documentation.

#### **graph\_button:**

This widget uses the v.Select() widget. It allows the user to switch between the different types of plots available. This widget's input is dependent on the \_data\_choices dictionary. So whatever dataset is chosen, the list of available visualizations of that dataset are loaded into the widget as the available options. For more detail on each plot, please see the [Visualizations](./README.md#Visualizations) section.

#### **user\_dropdown:**

This widget uses the v.Select() widget and allows the user to select which pre-made gene list they wish to explore. The user\_dropdown widget's input is dependent on the **\_user\_dropdown\_options dictionary** which contains all of the available gene ID or UniProt ID pathways. Once a pathway is selected, the gene/Uniprot ID's included in that pathway are inserted into the **user\_input** widget via using the ID list stored in the **\_user\_input dictionary** that correspond to that pathway.

#### **multicovariate\_selector:**

This widget uses the v.Select() widget and allows the user to select which covariates they wish to use in their visualization. This widget allows the user to **select multiple covariates at the same time**. It is only used for the Clustermap visualization.

#### **covariate\_selector:**

This widget uses the v.Select() widget and allows the user to select which covariate they wish to use in their visualization. This widget allows the user to select **only one covariates at a time**. It is used in all other visualizations when applicable.

#### **pca\_covariate\_selector:**

This widget uses the v.Select() widget and allows the user to select which covariate they wish to use in their visualization. This widget allows the user to select **only one covariates at a time**. It is used specifically for the PCA plots.

#### **norm\_selector:**

This widget uses the v.Select() widget. It allows the user to switch between the different types normalization options that are available which are detailed in the [Normalization](./README.md##Normalization) Section.

### [Panel Widgets](https://panel.holoviz.org/reference/index.html#widgets "Panel")

### **user\_input:**

This widget uses the [TextAreaInput widget](https://panel.holoviz.org/reference/widgets/TextAreaInput.html "TextAreaInput"). Its input is free to be customized by the user, meaning the user can input a gene list themselves manually.
Its input is directly taken from the **\_user\_input dictionary** when a gene or protein pathway is selected.
**Note**: In the future,we will be adding an upload gene list option.

### **participant\_input:**

This widget uses the [TextAreaInput widget](https://panel.holoviz.org/reference/widgets/TextAreaInput.html "TextAreaInput"). Its input is free to be customized by the user, meaning the user can input a participant list on their own if they wish. This widget directly takes input from the Answer ALS Data Portal. All partcipants selected from the data portal are automatically loaded in as the input to this widget. This is done via the requests python package which allows us to parse the json datafile sent through the URL.

### **p\_value\_input:**

This widget uses the [FloatInput widget](https://panel.holoviz.org/reference/widgets/FloatInput.html "FloatInput"). It allows the user to choose a p-value from a range of 0.05 to 1. By default, it starts out with 0.05 as a p-value. This widget only appears on certain visualizations like the volcano plot. The value chosen for this widget allows the user to set the threshold for significance.

### **log2FC\_input:**

This widget uses the [FloatInput widget](https://panel.holoviz.org/reference/widgets/FloatInput.html "FloatInput"). It allows the user to choose a log2(Fold Change) from a range of 1.5 to 5. By default, it starts out with 1.5 as the Log2FC value. This widget only appears on certain visualizations like the volcano plot. The value chosen for this widget allows the user to set the threshold for significance.

### **positive\_col:**

This widget uses the [ColorPicker widget](https://panel.holoviz.org/reference/widgets/ColorPicker.html "ColorPicker") to allow the usee to select which color they wish positive values to appear as on a plot. By default, it is set to visualize positive values as blue (hex:#1e7333). The user is allowed to select any color via the eye dropper tool included in the widget or by manually input the RGB values. This widget is only used in the Clustermap Visualization.

### **negative\_col:**

This widget uses the [ColorPicker widget](https://panel.holoviz.org/reference/widgets/ColorPicker.html "ColorPicker") to allow the usee to select which color they wish negative values to appear as on a plot. By default, it is set to visualize positive values as blue (hex:#1e7333). The user is allowed to select any color via the eye dropper tool included in the widget or by manually input the RGB values.

## Callback Functions
These are callback functions that define the backend behavior when a certain widget or button is clicked. These functions are all located in the utils.py script in the modules folder. 

#### **\_update\_input:**

This is a updating function that basically tells the computer to keep track of the user\_dropdown widget and makes sure that if the user selects a pathway, it updates the user\_input widget with the gene/protein pathway stored in the **\_user\_input dictionary**.

#### **switch\_data:**

This is an update function that does all the backend for switching datasets. It makes sure that all of the widgets update accordingly to each dataset and makes sure that no participants that are not included in the newly selected dataset are carried over.

#### **load\_plot:**

This function is reponsible for making sure the correct graph is loaded onto the main page for the visualization tool. It essentially checks which plot is selected in the graph\_button widget, and then grabs the correct visualization and puts that onto the main page of the tool.

#### **\_update\_plot:**

This helper function makes sure that all plots are updated with the current options selected by the wigdets. It is specifically dependent on the following widgets:

- multicovariate\_selector
- covariate\_selector
- pca\_covariate\_selector
- norm\_selector

### Normalizations

#### **normalize**

This function is where we formally define all of the normalization options and their calculations associated with each method. Currently,we support the following normalization methods:

- **None**
  - This option allows the user to plot raw counts without any normalization done to the data, besides the base conversion to TPM's.
- **Log Norm**
  - This option allows users to log10(1+x) normalize the data to deal with the 0 values in the data.
  - Note: In the future, we plan on offering different options for users to choose how they wish to deal with the 0's in the data.
- **Z-Score**
  - This option allows the user to perform the Z-score normalization on the data. This normalization is carried out using the scipy stats package, specifically their [zscore function](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.zscore.html "zscore").
- **Quantile Norm**
  - This option allows users to perform a Quantile normalization on the data. This normalization is carrioud out by sorting the data, then calculating the mean, and then using the rank function of dataframes in pandas, with method set to min.

### SQL Querying

SQL querying works using ODBC Driver 17 for SQL Server provided by Microsoft. You need to make sure you have this installed prior to running, otherwise you will not have access to the data. We use the pyodbc package here to connect the code to the SQL database. All of these functions are located in the sql.py file in the modules folder. 

#### **tpm\_sql\_query:**

This function queries the TPM data for transcriptomics data from the data sql database.

#### **de\_sql\_query:**

This function queries the differentially expressed data for transcriptomics data from the de\_data sql database.

#### **cov\_sql\_query:**

This function queries the covariates from the covariates sql database.

#### **protein\_sql\_query:**

This function queries the proteomics data from the protein\_level database.

#### **protein\_de\_sql\_query:**

This function queries the differentially expressed data for proteomics data from the protein\_de sql database.

## Visualizations
Each visualization has its own module folder within the modules folder. Within each folder lies the respective callbacks, widgets and unique sidebar panel if there is one for each visualization. 

#### **clustermap:**

This function is reponsible for carrying out all preprocessing the data and actually plotting the preprocessed data in a clustermap. This plot uses the [Clustergrammer2 package](https://clustergrammer.readthedocs.io/clustergrammer_widget.html "Clustergrammer2")

#### **boxplot:**

This function is reponsible for plotting the boxplot visualization. It uses the [Boxplot plotly package](https://plotly.com/python/box-plots/ "Boxplot").

#### **volcano\_plot:**

This function is reponsible for plotting the volcano visualization. It uses the [Volcano plotly package](https://plotly.com/python/volcano-plot/ "Volcano").

#### **pca\_plot\_2d:**

This function is reponsible for plotting the PCA 2D visualization. It uses the [PCA 2D plotly package](https://plotly.com/python/pca-visualization/ "PCA 2D").

#### **pca\_plot\_3d:**

This function is reponsible for plotting the PCA 3D visualization. It uses the [PCA 3D plotly package](https://plotly.com/python/pca-visualization/ "PCA 3D").

#### **dotplot:**

This function is reponsible for plotting the dotplot visualization. It uses the [Dotplot plotly package](https://plotly.com/python/dot-plots/ "Dot Plot").

#### **violinplot:**

This function is reponsible for plotting the dotplot visualization. It uses the [Violin Plot plotly package](https://plotly.com/python/violin/ "Violin Plot").

#### **distplot:**

This function is reponsible for plotting the dotplot visualization. It uses the [Distribtion Plot plotly package](https://plotly.com/python/distplot/ "Distribution Plot").

#### **protein\_pca\_plot\_2d:**

This function is reponsible for plotting the PCA 2D visualization for protein data. It uses the [PCA 2D plotly package](https://plotly.com/python/pca-visualization/ "PCA 2D").

#### **protein\_pca\_plot\_3d:**

This function is reponsible for plotting the PCA 3D visualization for protein data. It uses the [PCA 3D plotly package](https://plotly.com/python/pca-visualization/ "PCA 3D").

---

## Differential Expression Analysis Module

This module is designed to perform differential expression analysis using DESeq2. It integrates data querying, preprocessing, statistical analysis, and visualization into an interactive and user-friendly interface. Below is a detailed description of each file and its functionality.

---

## **Introduction**

The Differential Expression Analysis Module is part of the **Answer ALS Visualization Tool**, which provides users with a comprehensive environment for analyzing transcriptomic and proteomic datasets. It includes support for querying data from SQL databases, applying DESeq2 for differential expression analysis, and visualizing results using interactive plots.

---

## \*\*File: \*\***`transcriptomics_deseq.py`**

### Description:

This script performs differential expression analysis using DESeq2, integrating data querying, preprocessing, and visualization steps.

### Key Functionalities:

1. **Data Loading and Cleaning:**

   - Queries raw data and metadata from SQL using participant and user inputs.
   - Filters and aligns metadata and count data by participant IDs.

2. **DESeq2 Analysis:**

   - Constructs a `DeseqDataSet` object using preprocessed data.
   - Executes the DESeq2 pipeline and performs statistical analysis.

3. **Visualization:**

   - Creates an interactive scatter plot with fold-change and p-value statistics.
   - Annotates significant genes as "Upregulated," "Downregulated," or "Not Significant."

### Dependencies:

- Libraries: `numpy (np)`, `panel (pn)`, `plotly.express (px)`
- External modules: `modules.default`, `modules.sql`
- `pydeseq2` library for differential expression analysis.

### Outputs:

- An interactive volcano plot highlighting gene expression changes.



---

## Custom Groupings Module

This module enables users to create and manage custom groupings within the application, providing an interactive interface for defining, editing, and saving groupings.

---

## **File: `custom_groupings_widgets.py`**

### Description:
Defines widgets and layouts for creating and managing custom groupings within the application.

### Key Functionalities:
1. **Custom Grouping Creation Widgets:**
   - `ccgm_grouping_name`: Text input for naming the custom grouping.
   - `ccgm_num_groups`: Input field to define the number of subgroups.
   - `ccgm_custom_group_guide`: A step-by-step instructional guide for creating custom groupings.
   - `ccgm_close_modal_btn`: A button to submit and save custom groupings.

2. **Custom Grouping Layout:**
   - Organizes the guide, input fields, and buttons into a visually structured layout for ease of use.

3. **Edit Custom Groupings Widgets:**
   - `ecgm_custom_group_guide`: Provides guidance for editing custom groupings via an interactive data table.
   - `ecgm_close_modal_btn`: Button to save edits.

4. **Modal Management:**
   - `ccgm_open_modal_btn` and `ecgm_open_modal_btn`: Buttons to open modals for creating or editing custom groupings.

---

## **File: `callbacks.py`**

### Description:
Implements callback functions to manage the behavior of custom grouping modals and update UI elements dynamically.

### Key Functionalities:
1. **Widget Update and Validation:**
   - `update_ccgm_group_widgets`: Dynamically creates input fields for group names and participants based on the number of subgroups specified.

2. **Modal Management Callbacks:**
   - `open_ccgm_callback`: Opens the modal for creating custom groupings.
   - `open_ecgm_callback`: Opens the modal for editing existing custom groupings.

3. **Data Handling:**
   - `close_ccgm_callback`: Saves custom group information to a global DataFrame and updates relevant dropdown selectors.
   - `close_ecgm_callback`: Finalizes edits and ensures changes reflect in the UI.

4. **UI Notifications:**
   - Provides success or error notifications based on user actions, enhancing the user experience.

5. **Integration with UI Components:**
   - Links widgets to callbacks, ensuring dynamic updates based on user input or actions.

---

## **Overall Module Purpose**
This module simplifies the process of managing custom groupings by:
1. Providing a structured UI for creating and editing groups.
2. Ensuring seamless integration with existing dropdown selectors and plots.
3. Enhancing user experience with notifications and dynamic updates.

---

For any questions or further details, please refer to the specific file documentation or contact the development team.


