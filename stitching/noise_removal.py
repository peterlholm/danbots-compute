import numpy as np
import open3d as o3d


# Limit is ratio of total points in a cluster required to keep it.
def keep_significant_clusters(pcd, limit=0.06, eps=0.35, min_points=7):
    pcd_result = o3d.geometry.PointCloud()
    clusters = pcd.cluster_dbscan(eps, min_points)
    #print("a")
    # Messy way to count how many points are in each cluster.
    cluster_indicies = np.array(clusters) + 1
    # Bincount only counts non-negative.
    cluster_indicies_count = np.bincount(cluster_indicies)
    ii = np.nonzero(cluster_indicies_count)[0]
    # (ii - 1) corrects the one added above.
    #print("b")
    counts = zip(ii-1, cluster_indicies_count[ii])
    #print("counts", counts)
    kept_indicies = []
    for (cluster, count) in counts:
        if cluster == -1:  # Skip the noise.
            #print("skip", count)
            continue
        #print(count)
        kept = count / len(pcd.points)
        if kept >= limit:
            #print("kept", kept, "limit", limit)
            indicies = get_cluster_indicies(clusters, cluster)
            #print("inde", indicies)
            kept_indicies += indicies
            #print("kept:ind", kept_indicies)
            pcd_result += pcd.select_by_index(indicies)
            #print("inserted")
        else:
            pass
            #print("drop")
    #print("ud")
    return (pcd_result, kept_indicies)


def get_cluster_indicies(clusters, cluster):
    #print("get_cluster_indices")
    return [i for i, x in enumerate(clusters) if x == cluster]
