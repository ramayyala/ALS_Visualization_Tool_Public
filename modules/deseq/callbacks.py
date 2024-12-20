from modules.config import material 
from modules.deseq import deseq_widgets, transcriptomics_deseq
from modules.libraries import pn


def _deseq_update_plot(deseq_run_btn, event, data):
    print("running deseq analysis")
    material.main[0].objects = [pn.Row(transcriptomics_deseq.deseq(), height=1000)]


deseq_widgets.deseq_run_btn.on_event("click", _deseq_update_plot)
