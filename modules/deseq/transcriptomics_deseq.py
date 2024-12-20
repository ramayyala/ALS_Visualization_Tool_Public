from modules.default import general_widgets
from modules.libraries import np, pn, px
from pydeseq2.dds import DeseqDataSet
from pydeseq2.default_inference import DefaultInference
from pydeseq2.ds import DeseqStats
from modules.sql import _sql


def deseq():
    df_selected, gene_ids = _sql.de_fly_query(
        general_widgets.user_input.v_model, general_widgets.participant_input.v_model
    )
    df_selected = df_selected.T.rename_axis("Participant_ID")

    # metadata load
    metadata = _sql.cov_sql_query(general_widgets.covariate_selector.v_model)
    metadata.reset_index(inplace=True)
    metadata = metadata[metadata["Participant_ID"].isin(df_selected.index)]
    metadata.set_index("Participant_ID", inplace=True)
    # reorder the participant index ids so they follow the same order
    metadata = metadata.reindex(df_selected.index)
    pn.state.notifications.info("raw data and metadata loaded", duration=3000)
    samples_to_keep = ~metadata[general_widgets.covariate_selector.v_model].isna()
    df_selected = df_selected.loc[samples_to_keep]
    metadata = metadata.loc[samples_to_keep]
    pn.state.notifications.info("cleaning data", duration=3000)
    # create dds object
    inference = DefaultInference(n_cpus=1)
    dds = DeseqDataSet(
        counts=df_selected,
        metadata=metadata,
        design_factors=general_widgets.covariate_selector.v_model,
        refit_cooks=True,
        inference=inference,
    )
    pn.state.notifications.info("Deseq Object Created", duration=3000)
    # carry out differential expression analysis
    dds.deseq2()
    pn.state.notifications.info("Deseq Analysis Complete", duration=3000)
    print(dds)
    stat_res = DeseqStats(dds, inference=inference)
    pn.state.notifications.info("Statistical Analysis Complete", duration=3000)
    stat_res.summary()
    pn.state.notifications.info("Wald Test Complete", duration=3000)
    pn.state.notifications.success(
        "Different Expression Analysis Complete", duration=3000
    )
    df_selected = stat_res.results_df
    # merge gene ids in
    df_selected.rename(columns={"Geneid": "Ensembl_ID"}, inplace=True)
    print(gene_ids)
    df_selected = df_selected.merge(gene_ids, on="Ensembl_ID")
    df_selected["group"] = "Not Significant"
    fc_cutoff = general_widgets.log2FC_input.v_model
    p_cutoff = general_widgets.p_value_input.v_model
    df_selected.loc[
        (df_selected["log2FoldChange"] >= fc_cutoff)
        & (df_selected["pvalue"] < p_cutoff),
        "group",
    ] = "Upregulated"
    df_selected.loc[
        (df_selected["log2FoldChange"] <= fc_cutoff)
        & (df_selected["pvalue"] < p_cutoff),
        "group",
    ] = "Downregulated"
    df_selected["-log10(pvalue)"] = -np.log10(df_selected["pvalue"].clip(lower=1e-10))
    print(df_selected)
    fig = px.scatter(
        df_selected,
        x="log2FoldChange",
        y="-log10(pvalue)",
        color="group",
        width=1250,
        height=1000,
        hover_data=["geneids"],
    )
    fig.add_hline(y=-np.log(p_cutoff), line_dash="dash", line_color="black")
    fig.add_vline(x=fc_cutoff, line_dash="dash", line_color="black")
    fig.add_vline(x=-fc_cutoff, line_dash="dash", line_color="black")
    return fig
