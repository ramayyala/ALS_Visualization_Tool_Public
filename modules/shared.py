from modules.libraries import pn

pn.extension(
    "ipywidgets",
    "plotly",
    "tabulator",
    notifications=True,
    disconnect_notification="Connection lost, try reloading the page!",
    ready_notification="Application fully loaded.",
)

material = pn.template.BootstrapTemplate(
    site_url="https://dataportal.answerals.org/search",
    logo="misc/logo.png",
    title="ANSWER ALS VISUALIZATION TOOL",
    header_background="#204cac",
    sidebar_width=500,
)
