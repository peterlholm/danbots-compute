import numpy as np
import open3d as o3d


# Limit is ratio of total points in a cluster required to keep it.
def keep_significant_clusters(pcd, limit=0.06, eps=0.35, min_points=7):
    pcd_result = o3d.geometry.PointCloud()
    clusters = pcd.cluster_dbscan(eps, min_points)

    # Messy way to count how many points are in each cluster.
    cluster_indicies = np.array(clusters) + 1
    # Bincount only counts non-negative.
    cluster_indicies_count = np.bincount(cluster_indicies)
    ii = np.nonzero(cluster_indicies_count)[0]
    # (ii - 1) corrects the one added above.
    counts = zip(ii-1, cluster_indicies_count[ii])
    kept_indicies = []
    for (cluster, count) in counts:
        if cluster == -1:  # Skip the noise.
            continue
        kept = count / len(pcd.points)
        if kept >= limit:
            indicies = get_cluster_indicies(clusters, cluster)
            kept_indicies += indicies
            pcd_result += pcd.select_by_index(indicies)
    return (pcd_result, kept_indicies)


def get_cluster_indicies(clusters, cluster):
    return [i for i, x in enumerate(clusters) if x == cluster]
