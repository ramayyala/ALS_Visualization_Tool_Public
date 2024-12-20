from modules.boxplot import boxplot_plot
from modules.default import general_widgets, options_panel
from modules.deseq import deseq_options_panel
from modules.libraries import pn, v
from modules.shared import material

viz_tab = v.Tab(children=["Visualization"])
deseq_tab = v.Tab(children=["Differential Expression"])
eda_tab = v.Tab(children=["EDA"])
changelog_tab = v.Tab(children=["Changelog"])
feedback_tab = v.Tab(children=["Feedback"])


def _viz_tab_update(widget, event, data):
    print("switch to viz tab")
    material.sidebar[0].objects = [pn.Column(options_panel.options_panel)]
    material.main[0].objects = [pn.Row(boxplot_plot.boxplot(), height=1000)]


def _deseq_tab_update(deseq_tab, event, data):
    print("switch to deseq tab")
    material.sidebar[0].objects = [pn.Column(deseq_options_panel.deseq_options_panel)]
    material.main[0].objects = []


viz_tab.on_event("click", _viz_tab_update)
deseq_tab.on_event("click", _deseq_tab_update)


tabs_main_page = v.Tabs(
    children=[viz_tab, deseq_tab, eda_tab, changelog_tab, feedback_tab]
)
header_test = v.Container(
    style_="background-color: #204CAC", children=[v.Row(children=[tabs_main_page])]
)
material.header.append(header_test)
