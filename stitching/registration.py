import open3d as o3d
import numpy as np


def compute_normal(pcd):
    # creates normalts that all point in same (wrong) direction (due to low
    # radius).
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
              radius=0.1, max_nn=30))
    normals_load = np.asarray(pcd.normals) * -1  # Flip normals.
    pcd.normals = o3d.utility.Vector3dVector(normals_load)
    # Get new and correctly orientated normals.
    pcd.estimate_normals()


def preprocess_point_cloud(pcd, voxel_size):
    pcd_down = pcd.voxel_down_sample(voxel_size)

    compute_normal(pcd_down)

    radius_feature = voxel_size * 5
    pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd_down,
        o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
    return pcd_down, pcd_fpfh


def execute_global_registration(source_down, target_down, 
                                source_fpfh, target_fpfh, 
                                voxel_size, dist_thres_scalar=1.5, 
                                scale=False, edge_length_thres=0.99, 
                                converge_itr=(10**8),
                                converge_certainty=0.9999):
    distance_threshold = voxel_size * dist_thres_scalar
    result = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh, True,
        distance_threshold,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(scale),
        3, [
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(
                edge_length_thres),
            o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(
                distance_threshold)
        ], o3d.pipelines.registration.RANSACConvergenceCriteria(
            converge_itr, converge_certainty))
    return result


def execute_local_registration(source_down, target_down, voxel_size, 
                               init_transformation, converge_max_itr=30):
    conver_crit = o3d.pipelines.registration.ICPConvergenceCriteria()
    conver_crit.max_iteration = converge_max_itr
    result_icp = o3d.pipelines.registration.registration_icp(
                    source_down, target_down, voxel_size, init_transformation,
                    o3d.pipelines.registration.TransformationEstimationPointToPlane(),
                    criteria=conver_crit)
    return result_icp


def prepare_dataset(source, target, voxel_size):
    source_down, source_fpfh = preprocess_point_cloud(source, voxel_size)
    target_down, target_fpfh = preprocess_point_cloud(target, voxel_size)
    return source_down, target_down, source_fpfh, target_fpfh


def get_transformations(pcds, voxel_size):
    n = len(pcds)
    pivot = n // 2
    target = o3d.geometry.PointCloud() + pcds[pivot]
    transformations = []
    # Process from middle (pivot) and out.
    processing_order = sorted(range(n), key=lambda i: abs(pivot-i))
    for i in processing_order:
        if i == pivot:
            transformations.append(np.identity(4))
            continue
        else:
            source_down, target_down, source_fpfh, target_fpfh = \
                prepare_dataset(pcds[i], target, voxel_size)
            
            result_ransac = execute_global_registration(
                    source_down, target_down, source_fpfh, target_fpfh,
                    voxel_size)
            
            result_icp = execute_local_registration(
                    source_down, target_down, 
                    voxel_size, result_ransac.transformation)

            transformations.append(result_icp.transformation)
            source_down.transform(result_icp.transformation)
            target += source_down
            target = target.voxel_down_sample(voxel_size)
    return pcds, [transformations[i] for i in np.argsort(processing_order)]
