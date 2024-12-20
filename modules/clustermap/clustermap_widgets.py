import ipyvuetify as v

# Linkage and Distance Pickers for Clustermap
distance_selector = v.Select(
    style_="width: 400px",
    outlined=True,
    label="",
    items=[
        "canberra",
        "cityblock",
        "correlation",
        "cosine",
        "euclidean",
        "hamming",
        "jaccard",
        "minkowski",
        "mahalanobis",
        "seuclidean",
    ],
    v_model="euclidean",
    chips=True,
)
# NOTE: If distance metric is not euclidean, then ward, centroid, and median methods cannot be selected as the
# resulting hierarchical clustering will be incorrect
linkage_selector = v.Select(
    style_="width: 400px",
    outlined=True,
    label="",
    items=["average", "centroid", "complete", "median", "single", "weighted", "ward"],
    v_model="ward",
    chips=True,
)
