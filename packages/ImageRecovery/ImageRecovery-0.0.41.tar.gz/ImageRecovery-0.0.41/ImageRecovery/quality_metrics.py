import copy
import os

from sklearn.neighbors import NearestNeighbors
from collections import defaultdict
from scipy.spatial import Delaunay
import math
import pandas as pd
import ast
import csv
from scipy.stats import kurtosis

import matplotlib
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from matplotlib import cm
from matplotlib.transforms import Bbox
import pycpd
import random


from random_proximity_graphs import *

def generate_points(L, numb_points, dim):
    """""
    Creates scattered points in a square (dim=2) or cube (dim=3).
    dim: Dimension
    L: Edge size
    numb_points: System size
    """""

    # Initialize matrix, store the points positions
    positions_matrix = np.zeros((numb_points, dim))
    for ini in range(2):
        positions_matrix[ini] = np.zeros((1, dim))
    if dim == 3:
        positions_matrix[1]= np.array([0,0,L])
    elif dim == 2:
        positions_matrix[1][1] = L

    # for i in range(2 !!!) in 2d
    for i in range(2, numb_points):
        position = np.random.uniform(low=0, high=L, size=(dim,))
        for j in range(dim):
            positions_matrix[i][j] = position[j]

    positions_matrix = [str([element for element in row]) for row in positions_matrix]
    positions_df = pd.DataFrame(positions_matrix, columns=['POS'])
    positions_df['POS'] = positions_df['POS'].apply(ast.literal_eval)
    return positions_df

def write_positions_and_knn(L, numb_points, directory, k=10, radius=0.1, proximity_mode="knn", mode_3D=True,
                            scale_x=1, scale_y=1, prox_parameters=(1,1), weighting="unweight"):
    if mode_3D==True:
        dim = 3
    else:
        dim = 2
    positions_df = generate_points(L, numb_points, dim)
    positions = np.array(positions_df).tolist()
    distances, indices, indices_knn = get_proximity_graph(positions_df, k, radius, proximity_mode, scale_x=scale_x, scale_y=scale_y, prox_parameters=prox_parameters)
    distances, indices = [element.tolist() for element in distances], [element.tolist() for element in indices]
    indices = [[index+1 for index in vector] for vector in indices]   # Avoid starting at 0

    # Weighting
    if weighting == "unweight":
        weights = [[1 for distance in vector] for vector in distances]
    elif weighting == "softmax_inverse_distance":
        weight_function = lambda t: np.exp(-t)  # --> softmax inverse distance seem to work very well! As opposed to inverse distance, or inverse squared
        vfunc = np.vectorize(weight_function)
        weights = [[(np.exp(-distance))/np.sum(vfunc(np.array(vector))) for distance in vector] for vector in distances]

    elif weighting == "inverse_distance":
        # Artificial normalized weight obtained as distance^-2, exp(-distance)... (has to be the same as weight_function)
        weights = [[1/distance for distance in vector] for vector in distances]
    else:
        raise ValueError("Please select a proper weighting parameter, e.g. weighting=unweight")

    # Write graph dataframe
    f = open(directory + '/Input_Documents/Positions_And_Neighbors/neighbors_data_' + str(dim)+"D_"
             +str(numb_points)+'_'+ proximity_mode+'.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['POS', 'NN', 'Ndist', 'Nweight'])

    for i in range(len(indices)):

        writer.writerow([positions[i][0], indices[i], distances[i], weights[i]])
    f.close()



def apply_literal_format_to_df(df):
    df['NN'] = df['NN'].apply(ast.literal_eval)  # need to literal eval
    df['Ndist'] = df['Ndist'].apply(ast.literal_eval)  # need to literal eval
    df['Nweight'] = df['Nweight'].apply(ast.literal_eval)
    df['POS'] = df['POS'].apply(ast.literal_eval)  # need to literal eval
    return df

def get_position_list(df):
    positions = df['POS']
    positions = positions.values.tolist()  # from df object to python list
    return positions

def get_proximity_graph(df, k=15, radius=0.1, proximity_mode="knn", prox_parameters=(1,1), scale_x=1, scale_y=1):
    positions = get_position_list(df)


    # COMPUTE K-NEAREST NEIGHBORS FOR LOCAL QUALITY METRIC
    # k determines the nearest neighbors cut-off (knn)
    nbrs = NearestNeighbors(n_neighbors=k).fit(positions)
    # return distances and corresponding indices
    distances_knn, indices_knn = nbrs.kneighbors(positions)
    # It computes distance to self: fix it by deleting the first column
    distances_knn = np.delete(distances_knn, 0, 1)
    indices_knn = np.delete(indices_knn, 0, 1)


    # COMPUTE PROXIMITY GRAPH NEIGHBORS AND ITS DISTANCES
    if proximity_mode == "knn" or proximity_mode == "knn_weighted":
        distances = distances_knn
        indices = indices_knn

    elif proximity_mode == "epsilon-ball":        # epsilon-ball graph
        nbrs = NearestNeighbors(radius=radius).fit(positions)
        distances, indices = nbrs.radius_neighbors(positions, sort_results=True)
        # Deleting self-counting distances and indexes
        distances = np.array([np.delete(distances[i], 0, 0) for i in range(len(distances))])
        indices = np.array([np.delete(indices[i], 0, 0) for i in range(len(indices))])
        average_degree = sum(len(element) for element in indices)/len(indices)
        print("AVERAGE DEGREE EPSILON-BALL:", average_degree)

    elif proximity_mode == "delaunay":      # delaunay graph
        distances, indices = get_delaunay_neighbors(positions)
        average_degree = sum(len(element) for element in indices)/len(indices)
        print("AVERAGE DEGREE DELAUNAY:", average_degree)

    else:  # Random rules
        def create_prox_graph_random_rules():
            nbrs = NearestNeighbors(radius=radius).fit(positions)

            distances, indices = nbrs.radius_neighbors(positions, sort_results=True)
            # Deleting self-counting distances and indexes
            distances = np.array([np.delete(distances[i], 0, 0) for i in range(len(distances))])
            indices = np.array([np.delete(indices[i], 0, 0) for i in range(len(indices))])
            distances, indices = reject_neighbors_based_on_distance(distances, indices, radius, proximity_mode, prox_parameters, scale_x=scale_x, scale_y=scale_y)
            average_degree = sum(len(element) for element in indices) / len(indices)
            print(radius)
            print(f"AVERAGE DEGREE {proximity_mode}", average_degree)
            return average_degree, distances, indices
        average_degree, distances, indices = create_prox_graph_random_rules()
        if average_degree < k-3:  # Guarantee average degree degree k \pm 3
            radius += 0.1
            average_degree, distances, indices = create_prox_graph_random_rules()
            print(f"AVERAGE DEGREE {proximity_mode}", average_degree)
    return distances, indices, indices_knn  # first instance refers to itself (e.g. for distance [0, d1], [0,d2]...

def get_rejection_probability_depending_on_distance(distance, radius, proximity_mode, prox_parameters, scale_x=1, scale_y=1):
    """ Probability to reject a neighbor given its distance
        Features 4 proximity graphs, which can be many more by adjusting parameters
        For now, the default parameters are defined in this function #TODO: generalize parameters as input
    """
    # acceptance_at_radius = 0.47693628 # When distance = radius, there is a 50% acceptance --> erf-1(0.5)=0.47693628, erf-1(0.75) = 0.81341985
    # sigma = radius/(np.sqrt(2)*acceptance_at_radius)
    # prob = erf(distance/(sigma*np.sqrt(2)))
    if proximity_mode == "beta_multimodal":
        a1,a2,b1,b2 = prox_parameters[0], prox_parameters[1], prox_parameters[2], prox_parameters[3]
        value_pdf = multimodal_beta_single_value(distance, a1, b1, a2, b2, scale_x, scale_y)
    elif proximity_mode == "weibull_decaying_1":
        parameter_k, parameter_lambda = prox_parameters[0], prox_parameters[1]
        value_pdf = weibull_distribution_single_value(parameter_k, parameter_lambda, distance, scale_x, scale_y)
    elif proximity_mode == "weibull_2":
        parameter_k, parameter_lambda = prox_parameters[0], prox_parameters[1]
        value_pdf = weibull_distribution_single_value(parameter_k, parameter_lambda, distance, scale_x, scale_y)
    elif proximity_mode == "weibull_3":
        parameter_k, parameter_lambda = prox_parameters[0], prox_parameters[1]
        value_pdf = weibull_distribution_single_value(parameter_k, parameter_lambda, distance, scale_x, scale_y)
    else:
        raise ValueError("Please input a valid proximity graph: knn, epsilon-ball, beta_multimodal, weibull_decaying_1,"
                         "weibull_2, weibull_3")
    prob = 1 - value_pdf  # Rejection probability
    return prob

def reject_neighbors_based_on_distance(distances, indices, radius, proximity_mode, prox_parameters, scale_x=1, scale_y=1):
    """ Delete nodes that are rejected on the list of indices/distances.
        Model: epsilon-ball_decaying"""
    for (id_node, node) in enumerate(distances):   # Iterate over every node in the distance array
        deletion_list = []  # List to store all indices that are getting deleted
        for (id_neighbor, distance) in enumerate(node):  # Iterate over every node's neighbor
            if random.random() <= get_rejection_probability_depending_on_distance(distance, radius, proximity_mode, prox_parameters, scale_x=scale_x, scale_y=scale_y):
                deletion_list.append(id_neighbor)
        if deletion_list:
            # Delete the symmetric pairs
            for i in range(len(deletion_list)):
                neighbor_index = indices[id_node][deletion_list[i]]  # neighbor index in the original node
                # id of the original node through the point nof view of the neighboring node
                pairwise_neighbor_id = np.where(indices[neighbor_index] == id_node)[0][0]
                # once we know the index we delete it in indices & distances arrays
                indices[neighbor_index] = np.delete(indices[neighbor_index], pairwise_neighbor_id)
                distances[neighbor_index] = np.delete(distances[neighbor_index], pairwise_neighbor_id)

            # Delete nodes in the deletion list
            distances[id_node] = np.delete(distances[id_node], deletion_list)
            indices[id_node] = np.delete(indices[id_node], deletion_list)
    return distances, indices

def get_delaunay_neighbors(positions):
    """TO DO: Delaunay neighbors: return index and distances"""
    tess = Delaunay(positions)  # positions format np.array([[0,0], [1,2], ...]) . Get tessalation done
    set_neighbors = get_delaunay_neighbors_set_format(tess)
    indices = from_set_to_nparray(set_neighbors)  # list of neighbor indices with np.array() format
    distances = [np.array([math.dist(positions[i], positions[j]) for j in indices[i]]) for i in range(len(indices))]

    return distances, indices

def get_delaunay_neighbors_set_format(tess):
    neighbors = defaultdict(set)

    for simplex in tess.simplices:
        for idx in simplex:
            other = set(simplex)
            other.remove(idx)
            neighbors[idx] = neighbors[idx].union(other)
    return neighbors

def from_set_to_nparray(set_item):
    nparray_item = [[] for element in set_item]
    # Fill array with set values in an ordered manner (order provided by key)
    for (k,v) in set_item.items():
        value_list = list(v)
        nparray_item[k] = value_list
    # Transform lists into arrays
    nparray_item = [np.array(element) for element in nparray_item]
    nparray_item = np.array(nparray_item)
    return nparray_item

def count_intersecting_elements_by_row(matrix_1, matrix_2):
    """""
    Given 2 arrays, compute their row-intersection.
    In other words, it counts how many "shared" elements there are between rows.
    Returns the number of intersections for each row, e.g. [5,6,2,4] in a 4x6 matrix
    Update: returns the fraction of intersections, e.g.    [0.8, 1, 0.33, 0.6] in a 4x6 matrix
    """""
    # 1- Iterate over row_1 and row_2 simultaneously with zip
    # 2- Compute the intersection1d. If we sum its length, we get the number of shared elements
    return [(len(np.intersect1d(row_1[:min(len(row_1), len(row_2))], row_2[:min(len(row_1), len(row_2))]))) / min(len(row_1), len(row_2))
            for row_1, row_2 in zip(matrix_1, matrix_2)]

def compare_neighbors(nn_indices_original, nn_indices_recon):
    # Count row similarity between two arrays (intersection)
    count_shared_neighbors = sum(count_intersecting_elements_by_row(nn_indices_original, nn_indices_recon))
    # Divide by size rows (# columns) to get the fraction of correct neighbors --> not necessary now, already divided in previous func
    fraction_knn = count_shared_neighbors / np.shape(nn_indices_original)[0]  # shape = NxD
    return fraction_knn

def sample_points(points, cut_off=1000):
    """""
    Gets the first cut_off = 1000 points of a list of points that have no special order 
    They should be considered (randomized)  
    """""
    N = len(points)

    if len(points) <= cut_off:
        cut_off = N

    step = int(N / cut_off)
    indices = np.arange(0,cut_off,step)
    sampled_points = np.array(points)[indices]
    return sampled_points

def compute_pairwise_distance(points):
    """""
    Given a numpy array of points compute their pairwise distance.
    It is stored in a distance matrix
    """""
    points = np.array([list(x) for x in points])
    points_a = points
    points_b = points

    # Compute pariwise distances
    pairwise_matrix = np.linalg.norm(points_a[:, None, :] - points_b[None, :, :], axis=-1)
    # Select unique elements --> matrix is symmetric and yields N², we want N(N-1)/2
    pairwise_matrix_tril_indices = np.tril_indices(len(points), k=-1) # offset of 1 to avoid diagonal
    pairwise_distance_list = pairwise_matrix[pairwise_matrix_tril_indices]
    return pairwise_distance_list

def compute_pearson(data):
    """""
    From a list of points: data = [x,y]
    Return pearson correlation.

    pearson correlation function
    Should we pick random points because of computational cost? Pairwise distances between points in the sample
    Number of interactions : N(N-1)/2

    1- Select 1000 random points (top threshold)
    2- Compute pairwise distances (just use for loop and euclidean distance)
    3- Store it in a file 1: distance_1, distance_2, ..., distance_N-1. Pop 1 from the list. Repeat
       This will be our x-values (just a column)
    4- Do the same for the reconstructed coordinates. Will be y-values
    """""

    input = list(zip(data[0], data[1]))
    x_simple = pd.DataFrame(input, columns=["X", "Y"])
    # spearman_matrix = x_simple.corr(method="spearman") # Changed to PEARSON as it makes more sense (linear relation)
    pearson_matrix = x_simple.corr(method="pearson")
    pearson_matrix = pearson_matrix.values  # convert df to numpy matrix
    pearson_corr = pearson_matrix[0][1]  # Column X, Row Y yields the pearson correlation between X and Y
    return pearson_corr

def linear_regression_from_np_arrays(x,y):
    """"Data Series x and y --> Type: numpy 1 x N array
        Returns
                linear regression coefficients: y = theta[0]*x + theta[1]
                MSE
                R²
    """
    #print(x)
    numb_elements = len(x)
    x = x.reshape(numb_elements, 1)
    X = np.append(x, np.ones((numb_elements, 1)), axis=1)
    y = y.reshape(numb_elements, 1)
    theta = np.linalg.inv(X.T.dot(X)).dot(X.T).dot(y)
    y_line = theta[0]*x + theta[1]  # Prediction

    # Finding MSE and R^2
    MSE = np.square(np.subtract(y, y_line)).mean()
    SSE = np.sum(np.square(np.subtract(y, y_line)))
    SSR = np.sum(np.square(np.subtract(y.mean(), y_line)))
    SST = SSR + SSE
    R_squared = SSR / SST

    return theta, MSE, R_squared

def compute_distortion(euclidean_data, mapped_data):
    points_a, points_b = euclidean_data, mapped_data
    distortion_array = np.apply_along_axis(np.linalg.norm, 1, points_a-points_b)  # Compute distance 1to1 between original and reconstructed points
    mean_distortion = np.mean(distortion_array)
    var_distortion = np.var(distortion_array)
    return mean_distortion, var_distortion, distortion_array

def get_knn_quality_metric(df, k, radius, embedded_positions):
    """
    Compute k-nearest-neighbors for both original and reconstructed points
    The intersection between them is the local quality metric (KNN)
    """

    distances_original, nn_indices_original, indices_knn_original = \
        get_proximity_graph(df, proximity_mode="knn", k=k, radius=radius)  # Original points

    distances_recon, nn_indices_recon, indices_knn_recon = \
        get_proximity_graph(embedded_positions, proximity_mode="knn", k=k,
                            radius=radius)  # Reconstructed points
    fraction_knn = compare_neighbors(indices_knn_original, indices_knn_recon)
    return fraction_knn

def get_cpd_quality_metric(df, embedded_positions):
    # Subsample to reduce complexity: Take 1000 random points for both original and reconstructed points
    sampled_data = map(sample_points, [get_position_list(df), get_position_list(embedded_positions)])

    pairwise_data = [compute_pairwise_distance(data) for data in sampled_data]  # Get pairwise distance in euclidean and reconstructed

    pearson_corr = compute_pearson(pairwise_data)  # Compute pearson correlation
    return pearson_corr, pairwise_data

def align_to_original_image(original_positions, embedded_positions, original_distances, embedded_distances, args):
    # ALLIGNMENT TO ORIGNAL IMAGE

    mapped_points = scale_embedding_to_match_original(original_distances, embedded_distances, embedded_positions)
    mapped_points = translate_embedding_to_origin(original_positions, mapped_points)

    dim = np.shape(original_positions)[1]
    if dim == 2:
        original_positions, mapped_points_registered, distortion_array = \
            get_aligned_cube_2D(original_positions, mapped_points)
    elif dim == 3:
        original_positions, mapped_points_registered, distortion_array = \
            get_aligned_cube_3D(original_positions, mapped_points)
    else:
        raise ValueError("Dimension of your vectors should be 2 or 3")

    if args["plot_mode"]:
        plot_distortion_lines(original_positions, mapped_points_registered,
                              distortion_array, args)  # If you want to plot heatmap of lines (original - reconstructed)
    mean_distortion = np.mean(distortion_array)
    kurtosis_distortion = kurtosis(distortion_array)
    print(f"mean_distortion: {np.mean(distortion_array)}, var_distortion: {np.var(distortion_array)}, kur_distortion: {kurtosis_distortion}")
    directory = os.getcwd()
    numb_nodes = len(original_positions[:, 0])

    emb_mode = args["embedding_mode"]
    man_mode = args["manifold_learning_mode"]
    prox_mode = args["proximity_mode"]
    emb_dim = args["embedded_dim"]

    # Write mapped points
    f = open(f"{directory}/Output_Documents/Distortion_Plot/mapped_pos_{emb_mode}_{man_mode}_N={numb_nodes}_dim={dim}_emb_dim={emb_dim}_{prox_mode}.csv", 'w')
    writer = csv.writer(f)
    for i in range(numb_nodes):
        writer.writerow([mapped_points_registered[i]])
    f.close()

    # Write original points
    f = open(f"{directory}/Output_Documents/Distortion_Plot/original_pos{emb_mode}_{man_mode}_N={numb_nodes}_dim={dim}_emb_dim={emb_dim}_{prox_mode}.csv", 'w')
    writer = csv.writer(f)
    for i in range(numb_nodes):
        writer.writerow([original_positions[i]])
    f.close()
    return mean_distortion

def scale_embedding_to_match_original(original_distances, embedded_distances, embedded_positions):
    theta, MSE, R_squared = linear_regression_from_np_arrays(original_distances, embedded_distances)
    scaling_factor = theta[0]
    mapped_points = embedded_positions/scaling_factor
    return mapped_points

def translate_embedding_to_origin(original_positions, mapped_points):
    # # Translation
    t = (original_positions[0]) - (mapped_points[0])  # translation
    mapped_points = mapped_points + t
    return mapped_points

def get_aligned_cube_3D(original_positions, mapped_points):
    dim = np.shape(original_positions)[1]
    if dim != 3:
        raise ValueError('Vectors should be  3-dimensional')
    else:
        chiral_indices = np.array([[1,1,1],
                                   [1,-1,1],
                                   [1,1,-1],
                                   [1,-1,-1],
                                   [-1,1,1],
                                   [-1,-1,1],
                                   [-1,1,-1],
                                   [-1,-1,-1]
                                   ])
        original_positions_new = copy.deepcopy(original_positions)


        for i_x, i_y, i_z in chiral_indices:

            # Try different chiralities
            original_positions_new[:, 0] = i_x*original_positions[:, 0]
            original_positions_new[:, 1] = i_y*original_positions[:, 1]
            original_positions_new[:, 2] = i_z*original_positions[:, 2]
            # # Rotation

            vertical_vector_original = original_positions_new[0]-original_positions_new[1]
            vertical_vector_mapped = mapped_points[0]-mapped_points[1]
            rot_matrix = rotation_matrix_from_3d_vectors(vertical_vector_mapped, vertical_vector_original)
            mapped_points_new = np.dot(rot_matrix, mapped_points.T).T


            # Activate to plot registration
            mean_distortion, var_distortion, distortion_array = compute_distortion(original_positions_new, mapped_points_new)

            if mean_distortion < 1.5:

                # PYCPD: get better registration: use a sample of the points and get transformations
                reg = pycpd.AffineRegistration(**{'X': original_positions_new[:1000], 'Y': mapped_points_new[:1000]})   # Get a small sample (reduce computational burden
                mapped_points_small_sample, parameters = reg.register()
                rotation = parameters[0]
                translation = parameters[1]
                mapped_points_new = np.dot(mapped_points_new, rotation) + np.tile(translation,
                                                                                     (mapped_points_new.shape[0], 1))
                mean_distortion, var_distortion, distortion_array = compute_distortion(original_positions_new,
                                                                                       mapped_points_new)

                print("mean distortion after coherent point drift registration:", mean_distortion, "\nchirality indices:",
                      [i_x, i_y, i_z])
                if mean_distortion < 0.2:
                    print("Accepted mean distortion:", mean_distortion)
                    # Reverse coordinate change:
                    original_positions_new[:, 0] = i_x * original_positions_new[:, 0]
                    original_positions_new[:, 1] = i_y * original_positions_new[:, 1]
                    original_positions_new[:, 2] = i_z * original_positions_new[:, 2]
                    mapped_points_new[:, 0] = i_x * mapped_points_new[:, 0]
                    mapped_points_new[:, 1] = i_y * mapped_points_new[:, 1]
                    mapped_points_new[:, 2] = i_z * mapped_points_new[:, 2]
                    break

        else:
            print("3D alignment did not converge. Please try again with a different seed!")
            raise ValueError("3D alignment did not converge. Please try again with a different seed!")

    return original_positions_new, mapped_points_new, distortion_array

def get_aligned_cube_2D(original_positions, mapped_points):
    vertical_vector_original = original_positions[0] - original_positions[1]
    vertical_vector_mapped = mapped_points[0] - mapped_points[1]
    # # Rotation
    rot_matrix = rotation_matrix_2D(vertical_vector_mapped, vertical_vector_original)
    mapped_points = np.dot(rot_matrix, mapped_points.T).T

    # # Chirality
    mapped_points = check_chirality(mapped_points)

    # PYCPD: get better registration
    reg = pycpd.AffineRegistration(**{'X': original_positions[:1000], 'Y': mapped_points[:1000]})  # Threhsold 1000 for computational efficiency
    mapped_points_registered, parameters = reg.register()
    rotation, translation = parameters[:2]
    mapped_points_registered = np.dot(mapped_points, rotation) + np.tile(translation, (mapped_points.shape[0], 1))



    # Activate to plot registration
    mean_distortion, var_distortion, distortion_array = compute_distortion(original_positions, mapped_points_registered)

    return original_positions, mapped_points_registered, distortion_array

def rotation_matrix_from_3d_vectors(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 3d "source" vector
    :param vec2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    if s < 0.0001:    # Avoid singularity
        rotation_matrix = - np.eye(3)
    else:
        kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix

def rotation_matrix_2D(vec1, vec2):
    """ Find the rotation matrix that aligns vec1 to vec2
    :param vec1: A 2d "source" vector
    :param vec2: A 2d "destination" vector
    :return mat: A transform matrix (2x2) which when applied to vec1, aligns it with vec2.
    """
    dot_product = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    angle = np.arccos(dot_product)
    c, s = np.cos(angle), np.sin(angle)
    R = np.array(((c, -s), (s, c)))

    vec1 = R.dot(vec1)
    dot_product = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    angle_check = np.arccos(dot_product)

    if angle_check > 0.005:  # If not 0
        actual_angle = 2*np.pi - angle
        c, s = np.cos(actual_angle), np.sin(actual_angle)
        R = np.array(((c, -s), (s, c)))
        vec1_copy = R.dot(vec1)
    return R

def check_chirality(mapped_points):
    dim = len(mapped_points[0])
    if np.amin(mapped_points) < -0.7:  # Image is chiral
        for i in range(dim):
            if mapped_points[np.argmin(mapped_points, axis=0)[i]][i] < -0.7:  # Flip x, y, or z
                mapped_points[:, i] = -mapped_points[:, i]
    return mapped_points

def plot_distortion_lines(original_positions, mapped_points_positions, distortion_array, args):
    mean_distortion = np.mean(distortion_array)
    max_distortion = np.amax(distortion_array)
    min_distortion = np.amin(distortion_array)
    n_points = len(original_positions[:, 0])
    dim = len(original_positions[0, :])

    # To coompute colors
    norm = matplotlib.colors.Normalize(vmin=min_distortion, vmax=max_distortion)
    cmap = "Oranges"
    rgba_color_mean = cm.Oranges(norm(mean_distortion))
    rgba_color_max = cm.Oranges(norm(max_distortion))


    plt.style.use('science')
    fig = plt.figure(figsize=(6, 5))
    if dim == 2:
        ax = fig.add_subplot(111)
        for i in range(n_points):
            ax.plot([original_positions[:, 0][i],mapped_points_positions[:, 0][i]],
                    [original_positions[:, 1][i],mapped_points_positions[:, 1][i]],
                    c=cm.Oranges(norm(distortion_array[i])),
                    linewidth=2)
        scalebar_mean = AnchoredSizeBar(ax.transData,
                                        float(mean_distortion), 'mean distortion: %.2f' % mean_distortion,
                                        "upper center",
                                        pad=0.1,
                                        color=rgba_color_mean,
                                        frameon=False,
                                        size_vertical=0.01,
                                        bbox_to_anchor=Bbox.from_bounds(0, 0, 0.5, 1),
                                        bbox_transform=ax.figure.transFigure
                                        )

        scalebar_max = AnchoredSizeBar(ax.transData,
                                       max_distortion, 'max distortion: %.2f' % max_distortion, "upper center",
                                       pad=0.1,
                                       color=rgba_color_max,
                                       frameon=False,
                                       size_vertical=0.01,
                                       bbox_to_anchor=Bbox.from_bounds(0, 0, 0.5, 0.95),
                                       bbox_transform=ax.figure.transFigure
                                       )
    elif dim == 3:
        ax = fig.add_subplot(111, projection='3d')
        plt.axis('off')
        for i in range(n_points):
            ax.plot([original_positions[:, 0][i],mapped_points_positions[:, 0][i]],
                    [original_positions[:, 1][i],mapped_points_positions[:, 1][i]],
                    [original_positions[:, 2][i], mapped_points_positions[:, 2][i]],
                    c=cm.Oranges(norm(distortion_array[i])),
                    linewidth=1)
        typical_length = 0.05
        bar_height = 0.001
        scalebar_mean = AnchoredSizeBar(ax.transData,
                                        float(mean_distortion*typical_length), 'mean distortion: %.2f' % mean_distortion,
                                        "upper center",
                                        pad=0.1,
                                        color = "k", #color=rgba_color_mean,
                                        frameon=False,
                                        size_vertical=bar_height,
                                        bbox_to_anchor=Bbox.from_bounds(0, 0, 0.5, 1),
                                        bbox_transform=ax.figure.transFigure
                                        )

        scalebar_max = AnchoredSizeBar(ax.transData,
                                       max_distortion*typical_length, 'max distortion: %.2f' % max_distortion, "upper center",
                                       pad=0.1,
                                       color="k", #color=rgba_color_max,
                                       frameon=False,
                                       size_vertical=bar_height,
                                       bbox_to_anchor=Bbox.from_bounds(0, 0, 0.5, 0.95),
                                       bbox_transform=ax.figure.transFigure
                                       )

        scalebar_length = AnchoredSizeBar(ax.transData,
                                          1*typical_length, 'cube length %.2f' % 1, "upper center",
                                          pad=0.1,
                                          color="k", # color=rgba_color_max,
                                          frameon=False,
                                          size_vertical=bar_height,
                                          bbox_to_anchor=Bbox.from_bounds(0, 0, 0.5, 0.9),
                                          bbox_transform=ax.figure.transFigure
                                          )
        ax.add_artist(scalebar_length)
    else:
        raise ValueError('Vectors should be 2 or 3-dimensional')


    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm)

    ax.add_artist(scalebar_mean)
    ax.add_artist(scalebar_max)

    directory = os.getcwd()
    emb_mode = args["embedding_mode"]
    man_mode = args["manifold_learning_mode"]
    prox_mode = args["proximity_mode"]
    emb_dim = args["embedded_dim"]

    plt.savefig(f"{directory}/Output_Documents/Distortion_Plot/{emb_mode}_{man_mode}_N={n_points}_dim={dim}_emb_dim={emb_dim}_{prox_mode}_distortion_line.pdf")
    plt.show()

def main_function_quality_metrics(args, df, directory, embedding_mode, plot_vis, proximity_mode, k=15, radius=0.1, align_to_original=False):
    quality_metrics = {}
    # Get embedded/reconstructed positions
    embedded_positions = pd.read_csv(directory + '/Output_Documents/Embedded_Positions/embedded_pos_'
                                     + embedding_mode + '_' + plot_vis + '_'
                                     + str(args["density"])+'.csv')
    embedded_positions['POS'] = np.array(embedded_positions['POS'].apply(ast.literal_eval))

    if proximity_mode != "experimental":  # Synthetic data (proximity graphs, etc.)
        # Get original positions
        original_positions = np.array(df["POS"].tolist())
        # Local quality metric: K-Nearest Neighbors
        fraction_knn = get_knn_quality_metric(df, k, radius, embedded_positions)
        # Global quality metric: Pearson correlation
        pearson_corr, pairwise_data = get_cpd_quality_metric(df, embedded_positions)
        if not align_to_original:
            quality_metrics.update({"K": k, "KNN": fraction_knn, "CPD": pearson_corr})


        else:
            # Compute mean distoriton
            embedded_positions = np.array(get_position_list(embedded_positions))
            original_distances = pairwise_data[0]  # Pairwise distances in the original space
            embedded_distances = pairwise_data[1]  # Pairwise distances in the reconstructed space

            mean_distortion = align_to_original_image(original_positions, embedded_positions, original_distances,
                                                      embedded_distances, args)
            quality_metrics.update({"K": k, "KNN": fraction_knn, "CPD": pearson_corr,
                                    "Distortion": mean_distortion})
    else:    # Experimantal data
        quality_metrics.update({})

    return quality_metrics

