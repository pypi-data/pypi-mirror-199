import numpy as np
import pandas as pd
import csv
import os
import copy
import pycpd
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from matplotlib import cm
from matplotlib.transforms import Bbox
import matplotlib
from scipy.stats import kurtosis
import seaborn as sns
import probreg


def generate_points(L, numb_points, dim):
    """""
    Creates scattered points in a square (dim=2) or cube (dim=3).
    dim: Dimension
    L: Edge size
    numb_points: How many points
    """""

    # Initialize matrix, store the points positions
    positions_matrix = np.zeros((numb_points, dim))


    # # Establish fixed points to compute distortion
    # Create [0,0], [0,L] - 2D
    # Create [0,0,0], [0,L,0] -3D
    for ini in range(2):
        positions_matrix[ini] = np.zeros((1, dim))
    if dim == 3:
        positions_matrix[1]= np.array([0,0,L])
        column_values = ["x", "y", "z"]
    elif dim == 2:
        positions_matrix[1][1] = L
        column_values = ["x", "y"]

    # for i in range(2 !!!) in 2d
    for i in range(2, numb_points):
        position = np.random.uniform(low=0, high=L, size=(dim,))
        for j in range(dim):
            positions_matrix[i][j] = position[j]


    # positions_matrix = positions_matrix.tolist()    # Convert to list, necessary step to dataframe
    # positions_matrix = [str([element for element in row]) for row in positions_matrix]
    positions_df = pd.DataFrame(data=positions_matrix,
                      columns=column_values)
    half0_half1 = np.zeros((numb_points, 1)).astype(int)
    half0_half1[-int(numb_points/2):] = 1
    positions_df.insert(0, "beacon", half0_half1)
    positions_df.to_csv("posfile_for_weinstein_approach.csv", header=False)
    return positions_df





# Why do I need df for everything?! Should just do with original and reconstructed positions


def get_knn_proximity_graph(positions, k):


    # COMPUTE K-NEAREST NEIGHBORS FOR LOCAL QUALITY METRIC
    # k determines the nearest neighbors cut-off (knn)
    nbrs = NearestNeighbors(n_neighbors=k).fit(positions)
    # return distances and corresponding indices
    distances_knn, indices_knn = nbrs.kneighbors(positions)
    # It computes distance to self: fix it by deleting the first column
    distances_knn = np.delete(distances_knn, 0, 1)
    indices_knn = np.delete(indices_knn, 0, 1)
    return distances_knn, indices_knn, indices_knn

def count_intersecting_elements_by_row(matrix_1, matrix_2):
    """""
    Given 2 arrays, compute their row-intersection.
    In other words, it counts how many "shared" elements there are between rows.
    Returns the number of intersections for each row, e.g. [5,6,2,4] in a 4x6 matrix
    Update: returns the fraction of intersections, e.g.    [0.8, 1, 0.33, 0.6] in a 4x6 matrix
    """""
    # 1- Iterate over row_1 and row_2 simultaneously with zip
    # 2- Compute the intersection1d. If we sum its length, we get the number of shared elements
    # TODO: when len(row_1) != len(row_2) what criteria to use? e.g. row_2 > row_1
    #   a) Count which elements of row_1 are in row_2, average over len(row_1) --> If you want this delete the [:min(len(row_1), len(row_2))]
    #   b) Shorten row_2 so it has same length  --> Rank comparison more or less --> I choose this
    # Reasoning behind: graph data should never be "cut" because it would be random
    #                   however, knn data is ranked
    #                   we favor knn cutting as opposed to graph cutting
    # Why doesn't NGT KNN produce same results as KNN? Due to assymetry, graph KNN will have K+5 neighbors on average, changing a little how the metric behaves
    return [(len(np.intersect1d(row_1[:min(len(row_1), len(row_2))], row_2[:min(len(row_1), len(row_2))]))) / min(len(row_1), len(row_2))
            for row_1, row_2 in zip(matrix_1, matrix_2)]


def compare_neighbors(nn_indices_original, nn_indices_recon):
    # Count row similarity between two arrays (intersection)
    count_shared_neighbors = sum(count_intersecting_elements_by_row(nn_indices_original, nn_indices_recon))
    # Divide by size rows (# columns) to get the fraction of correct neighbors --> not necessary now, already divided in previous func
    fraction_knn = count_shared_neighbors / np.shape(nn_indices_original)[0]  # shape = NxD
    return fraction_knn

def get_knn_quality_metric(original_positions, embedded_positions, k):
    """
    Compute k-nearest-neighbors for both original and reconstructed points
    The intersection between them is the local quality metric (KNN)
    """

    distances_original, nn_indices_original, indices_knn_original = \
        get_knn_proximity_graph(original_positions, k=k)  # Original points

    distances_recon, nn_indices_recon, indices_knn_recon = \
        get_knn_proximity_graph(embedded_positions, k=k)  # Original points
    fraction_knn = compare_neighbors(indices_knn_original, indices_knn_recon)
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

    # # Plot distance matrices!!!
    # plt.figure(figsize=(14, 14))
    # # add heatmap
    # sns.heatmap(pairwise_matrix, cmap="plasma", yticklabels=False, xticklabels=False)
    # # save the figure
    # plt.savefig('test.png', dpi=600)
    # plt.show()


    # Select unique elements --> matrix is symmetric and yields N², we want N(N-1)/2
    pairwise_matrix_tril = np.tril(pairwise_matrix)  # Get the lower triangle
    pairwise_distance_list = pairwise_matrix_tril[np.nonzero(pairwise_matrix_tril)]  # Get lower triangle in a np array
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


def get_cpd_quality_metric(original_positions, embedded_positions):
    # Subsample to reduce complexity: Take 1000 random points for both original and reconstructed points
    sampled_data = map(sample_points, [original_positions, embedded_positions])
    pairwise_data = [compute_pairwise_distance(data) for data in sampled_data]  # Get pairwise distance in euclidean and reconstructed
    pearson_corr = compute_pearson(pairwise_data)  # Compute pearson correlation
    return pearson_corr, pairwise_data



def align_to_original_image(original_positions, embedded_positions, original_distances, embedded_distances):
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

    # # Kabsch umeyama
    # selected_indices = [0,1,2,3]
    # R, c, t = kabsch_umeyama(original_positions[selected_indices], embedded_positions[selected_indices])
    # mapped_points = np.array([t + c * R @ b for b in embedded_positions])

    # ACTIVATE TO PLOT!!!
    plot_original_and_mapped_points(original_positions, mapped_points_registered)
    # plot_distortion_reconstructed(mapped_points, distortion_array)             # If you want to plot heatmap of points
    plot_distortion_lines(original_positions, mapped_points_registered,
                          distortion_array)  # If you want to plot heatmap of lines (original - reconstructed)

    mean_distortion = np.mean(distortion_array)
    kurtosis_distortion = kurtosis(distortion_array)
    print(f"ATTENTION: mean_distortion: {np.mean(distortion_array)}, var_distortion: {np.var(distortion_array)}, kur_distortion: {kurtosis_distortion}")

    directory = os.getcwd()
    numb_nodes = len(original_positions[:, 0])

    # # Write mapped points
    # f = open(directory + '/Output_Documents/Distortion_Plot/mapped_pos_'+'N='+str(numb_nodes)+"dim="+str(dim)+'.csv', 'w')
    # writer = csv.writer(f)
    # for i in range(numb_nodes):
    #     writer.writerow([mapped_points_registered[i]])
    # f.close()
    #
    # # Write original points
    # f = open(directory + '/Output_Documents/Distortion_Plot/original_pos_'+'N='+str(numb_nodes)+"dim="+str(dim)+'.csv', 'w')
    # writer = csv.writer(f)
    # for i in range(numb_nodes):
    #     writer.writerow([original_positions[i]])
    # f.close()
    return mean_distortion

def plot_distortion_lines(original_positions, mapped_points_positions, distortion_array):
    # Normalize (L=100)
    L = 100
    distortion_array /= L
    original_positions /= L
    mapped_points_positions /= L
    mean_distortion = np.mean(distortion_array)
    max_distortion = np.amax(distortion_array)
    min_distortion = np.amin(distortion_array)
    n_points = len(original_positions[:, 0])
    dim = len(original_positions[0, :])
    log_distortion_array = np.log(distortion_array)
    plt.close()
    plt.figure()
    sns.distplot(log_distortion_array, hist_kws={'alpha': 0.7}, kde_kws={'linewidth': 3},  kde=False)
    plt.xlabel("log(distortion)")
    plt.ylabel("counts")
    #plt.xscale("log")
    plt.savefig("distortion_distribution_hist_weinstein.pdf")


    #plt.show()
    # To coompute colors
    norm = matplotlib.colors.Normalize(vmin=min_distortion, vmax=max_distortion)
    cmap = "Oranges"
    rgba_color_mean = cm.Oranges(norm(mean_distortion))
    rgba_color_max = cm.Oranges(norm(max_distortion))


    def plot_distortion_lines_helper():
        plt.style.use('science')
        fig = plt.figure(figsize=(6, 5))
        if dim == 2:
            ax = fig.add_subplot(111)
            for i in range(n_points):
                ax.plot([original_positions[:, 0][i], mapped_points_positions[:, 0][i]],
                        [original_positions[:, 1][i], mapped_points_positions[:, 1][i]],
                        c=cm.Oranges(norm(distortion_array[i])),
                        linewidth=2)
        elif dim == 3:
            ax = fig.add_subplot(111, projection='3d')
            plt.axis('off')
            for i in range(n_points):
                ax.plot([original_positions[:, 0][i], mapped_points_positions[:, 0][i]],
                        [original_positions[:, 1][i], mapped_points_positions[:, 1][i]],
                        [original_positions[:, 2][i], mapped_points_positions[:, 2][i]],
                        c=cm.Oranges(norm(distortion_array[i])),
                        linewidth=1)
            typical_length = 0.05
            bar_height = 0.001
            scalebar_mean = AnchoredSizeBar(ax.transData,
                                            float(mean_distortion * typical_length),
                                            'mean distortion: %.2f' % mean_distortion,
                                            "upper center",
                                            pad=0.1,
                                            color="k",  # color=rgba_color_mean,
                                            frameon=False,
                                            size_vertical=bar_height,
                                            bbox_to_anchor=Bbox.from_bounds(0, 0, 0.5, 1),
                                            bbox_transform=ax.figure.transFigure
                                            )

            scalebar_max = AnchoredSizeBar(ax.transData,
                                           max_distortion * typical_length, 'max distortion: %.2f' % max_distortion,
                                           "upper center",
                                           pad=0.1,
                                           color="k",  # color=rgba_color_max,
                                           frameon=False,
                                           size_vertical=bar_height,
                                           bbox_to_anchor=Bbox.from_bounds(0, 0, 0.5, 0.95),
                                           bbox_transform=ax.figure.transFigure
                                           )

            scalebar_length = AnchoredSizeBar(ax.transData,
                                              1 * typical_length, 'cube length %.2f' % 1, "upper center",
                                              pad=0.1,
                                              color="k",  # color=rgba_color_max,
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
        cbar = plt.colorbar(sm)
        cbar.ax.set_ylabel('distortion')


        # plt.close()

    # Plot without removing outliers
    plot_distortion_lines_helper()
    plt.savefig(f"distortion_line_weinstein.png", dpi=600)

    delete_outliers_condition = True
    # Remove outliers
    if delete_outliers_condition:
        print("total points", len(distortion_array))
        delete_outliers = np.where(distortion_array > 12/L) # Major part of outliers (5% of total) are length > 12
        print("len outliers", len(delete_outliers[0]))
        distortion_array = np.delete(distortion_array, delete_outliers, 0)
        mean_distortion_no_outliers = np.mean(distortion_array)
        max_distortion = np.amax(distortion_array)
        min_distortion = np.amin(distortion_array)
        norm = matplotlib.colors.Normalize(vmin=min_distortion, vmax=max_distortion)
        cmap = "Oranges"
        rgba_color_mean = cm.Oranges(norm(mean_distortion_no_outliers))
        rgba_color_max = cm.Oranges(norm(max_distortion))

        original_positions = np.delete(original_positions, delete_outliers, 0)
        mapped_points_positions = np.delete(mapped_points_positions, delete_outliers, 0)
        n_points = n_points-len(delete_outliers[0])
        plot_distortion_lines_helper()
        plt.savefig(f"distortion_line_weinstein_no_outliers.png", dpi=600)

    #plt.show()


def plot_original_and_mapped_points(original_positions, mapped_points_positions):
    mapped_points_positions = np.array(mapped_points_positions)

    dim = len(mapped_points_positions[0])

    fig = plt.figure()
    if dim == 2:
        ax = fig.add_subplot(111)
        ax.scatter(mapped_points_positions[:, 0], mapped_points_positions[:, 1], c="r" )
        ax.scatter(original_positions[:, 0], original_positions[:, 1], c="g")
        for i in range(len(original_positions)):
            ax.annotate(i, (original_positions[i][0], original_positions[i][1]))
            ax.annotate(i, (mapped_points_positions[i][0], mapped_points_positions[i][1]))
    elif dim == 3:
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(mapped_points_positions[:, 0], mapped_points_positions[:, 1], mapped_points_positions[:, 2], c="r" )
        ax.scatter(original_positions[:, 0], original_positions[:, 1], original_positions[:, 2], c="g")


        for i in range(4):
            ax.text(mapped_points_positions[:, 0][i], mapped_points_positions[:, 1][i], mapped_points_positions[:, 2][i], i, fontsize=12, color="red", fontweight="bold")
            ax.text(original_positions[:, 0][i], original_positions[:, 1][i], original_positions[:, 2][i], i, fontsize=12, color="green", fontweight="bold")

        # give the labels to each point
        # for x, y, z, label in zip(original_positions[:, 0], original_positions[:, 1], original_positions[:, 2], labels):
        #     ax.text(x, y, z, label)
        # for x, y, z, label in zip(mapped_points_positions[:, 0], mapped_points_positions[:, 1], mapped_points_positions[:, 2], labels):
        #     ax.text(x, y, z, label)
    #plt.show()

def scale_embedding_to_match_original(original_distances, embedded_distances, embedded_positions):
# # Scaling
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
            # Grab two known orthogonal vectors for the original and reconstructed
            vertical_vector_original = original_positions_new[0]-original_positions_new[1]
            vertical_vector_mapped = mapped_points[0]-mapped_points[1]
            rot_matrix = rotation_matrix_from_3d_vectors(vertical_vector_mapped, vertical_vector_original)
            mapped_points_new = np.dot(rot_matrix, mapped_points.T).T

            dot_product = np.dot(mapped_points_new[0]-mapped_points_new[1], vertical_vector_original) / \
                          (np.linalg.norm(mapped_points_new[0]-mapped_points_new[1]) * np.linalg.norm(vertical_vector_original))

            angle_check = np.arccos(dot_product)


            # # PYCPD: get better registration
            # reg = pycpd.AffineRegistration(**{'X': original_positions_new, 'Y': mapped_points_new})
            # #reg = pycpd.RigidRegistration(**{'X': original_positions, 'Y': mapped_points})
            # mapped_points_new, parameters = reg.register()

            # Activate to plot registration
            mean_distortion, var_distortion, distortion_array = compute_distortion(original_positions_new, mapped_points_new)

            if mean_distortion < 1.5:

                # PYCPD: get better registration: use a sample of the points and get transformations
                reg = pycpd.AffineRegistration(**{'X': original_positions_new[:1000], 'Y': mapped_points_new[:1000]})   # Get a small sample (reduce computational burden
                # reg = pycpd.RigidRegistration(**{'X': original_positions, 'Y': mapped_points})
                mapped_points_small_sample, parameters = reg.register()

                rotation = parameters[0]
                translation = parameters[1]
                mapped_points_new = np.dot(mapped_points_new, rotation) + np.tile(translation,
                                                                                     (mapped_points_new.shape[0], 1))
                mean_distortion, var_distortion, distortion_array = compute_distortion(original_positions_new,
                                                                                       mapped_points_new)


                if mean_distortion < 0.2:

                    # Reverse coordinate change:
                    original_positions_new[:, 0] = i_x * original_positions_new[:, 0]
                    original_positions_new[:, 1] = i_y * original_positions_new[:, 1]
                    original_positions_new[:, 2] = i_z * original_positions_new[:, 2]
                    mapped_points_new[:, 0] = i_x * mapped_points_new[:, 0]
                    mapped_points_new[:, 1] = i_y * mapped_points_new[:, 1]
                    mapped_points_new[:, 2] = i_z * mapped_points_new[:, 2]
                    break

        else:
            raise ValueError("3D alignment did not converge. Please try again with a different seed!")

    return original_positions_new, mapped_points_new, distortion_array

def get_aligned_cube_2D(original_positions, mapped_points):
    # Manual tweaks

    vertical_vector_original = original_positions[0] - original_positions[1]
    vertical_vector_mapped = mapped_points[0] - mapped_points[1]
    # # Rotation
    rot_matrix = rotation_matrix_2D(vertical_vector_mapped, vertical_vector_original)
    # for i, mapped_point in enumerate(mapped_points):
    #     mapped_points[i] = rot_matrix.dot(mapped_point)
    mapped_points = np.dot(rot_matrix, mapped_points.T).T

    # # Chirality
    mapped_points = check_chirality(mapped_points)
    dot_product = np.dot(mapped_points[0] - mapped_points[1], vertical_vector_original) / \
                  (np.linalg.norm(mapped_points[0] - mapped_points[1]) * np.linalg.norm(vertical_vector_original))

    angle_check = np.arccos(dot_product)

    # mapped_points = np.transpose(rot_matrix.dot(np.transpose(mapped_points)))



    chiral_indices = np.array([[1, 1],
                               [-1, 1],
                               [1, -1],
                               [-1, -1]])

    # # PROBERG (prob does the same as pycpd, the cpd algorithm)
    # tf_param, _, _ = probreg.cpd.registration_cpd(mapped_points, original_positions)
    # mapped_points_registered = copy.deepcopy(mapped_points)
    # mapped_points_registered = tf_param.transform(mapped_points_registered)

    # PYCPD: get better registration
    mean_distortion = 50

    for ix, iy in chiral_indices:

        auxiliary_mapped_points = copy.deepcopy(mapped_points)
        auxiliary_mapped_points[:,0] *= ix
        auxiliary_mapped_points[:, 1] *= iy

        # ## Pycpd registration
        # reg = pycpd.AffineRegistration(**{'X': original_positions[:1000], 'Y': auxiliary_mapped_points})  # Cap it to 1000 to not get long computational times
        # mapped_points_registered, parameters = reg.register()
        # rotation = parameters[0]
        # translation = parameters[1]
        # mapped_points_registered = np.dot(mapped_points, rotation) + np.tile(translation, (mapped_points.shape[0], 1))
        # mean_distortion, var_distortion, distortion_array = compute_distortion(original_positions,
        #                                                                        mapped_points_registered)

        # Try Umeyama:
        R, c, t = kabsch_umeyama(original_positions, auxiliary_mapped_points)
        auxiliary_mapped_points = np.array([t + c * R @ m_point for m_point in mapped_points])

        reg = pycpd.AffineRegistration(**{'X': original_positions[:1000],
                                          'Y': auxiliary_mapped_points[:1000]})  # Cap it to 1000 to not get long computational times
        dummy_points, parameters = reg.register()
        rotation = parameters[0]
        translation = parameters[1]
        mapped_points_registered = np.dot(auxiliary_mapped_points, rotation) + np.tile(translation, (auxiliary_mapped_points.shape[0], 1))
        mean_distortion, var_distortion, distortion_array = compute_distortion(original_positions,
                                                                               mapped_points_registered)

        if mean_distortion < 7:

            break



    # # Try Umeyama:
    # R, c, t = kabsch_umeyama(original_positions, mapped_points)
    # mapped_points_registered = np.array([t + c * R @ m_point for m_point in mapped_points])

    # Activate to plot registration
    mean_distortion, var_distortion, distortion_array = compute_distortion(original_positions, mapped_points_registered)

    return original_positions, mapped_points_registered, distortion_array


def kabsch_umeyama(A, B):
    """
    Kabsch–Umeyama algorithm is a method for aligning and comparing the similarity between two sets of points.
    It finds the optimal translation, rotation and scaling by minimizing the root-mean-square deviation (RMSD)
    of the point pairs.
    Input: A --> Original Points
           B --> Points to be registrated in A
    To apply  transformations simply do: B = np.array([t + c * R @ b for b in B])
    """
    assert A.shape == B.shape
    n, m = A.shape

    EA = np.mean(A, axis=0)
    EB = np.mean(B, axis=0)
    VarA = np.mean(np.linalg.norm(A - EA, axis=1) ** 2)

    H = ((A - EA).T @ (B - EB)) / n
    U, D, VT = np.linalg.svd(H)
    d = np.sign(np.linalg.det(U) * np.linalg.det(VT))
    S = np.diag([1] * (m - 1) + [d])

    R = U @ S @ VT
    c = VarA / np.trace(np.diag(D) @ S)
    t = EA - c * R @ EB
    return R, c, t

def check_chirality(mapped_points):
    # Check for chirality
    dim = len(mapped_points[0])

    if np.amin(mapped_points) < -0.7*100:  # Image is chiral

        for i in range(dim):
            if mapped_points[np.argmin(mapped_points, axis=0)[i]][i] < -0.7*100:  # Flip x, y, or z

                mapped_points[:, i] = -mapped_points[:, i]

    return mapped_points

def compute_distortion(euclidean_data, mapped_data):
    points_a, points_b = euclidean_data, mapped_data
    #pairwise_matrix = np.linalg.norm(points_a[:, None, :] - points_b[None, :, :], axis=-1)
    distortion_array = np.apply_along_axis(np.linalg.norm, 1, points_a-points_b)  # Compute distance 1to1 between original and reconstructed points
    mean_distortion = np.mean(distortion_array)
    var_distortion = np.var(distortion_array)
    return mean_distortion, var_distortion, distortion_array

def linear_regression_from_np_arrays(x,y):
    """"Data Series x and y --> Type: numpy 1 x N array
        Returns
                linear regression coefficients: y = theta[0]*x + theta[1]
                MSE
                R²
    """

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
    if s < 0.0001:    # Avoid dividing by 0
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
        dot_product = np.dot(vec1_copy, vec2) / (np.linalg.norm(vec1_copy) * np.linalg.norm(vec2))
        angle_check = np.arccos(dot_product)

    return R

def main_function_quality_metrics(original_positions, embedded_positions, k=15, align_to_original=False):
    """
    Should only need original and embedded positions!
    """
    quality_metrics = {}
    # Get embedded/reconstructed positions
    # embedded_positions = pd.read_csv(directory + '/Output_Documents/Embedded_Positions/embedded_pos_'
    #                                  + embedding_mode + '_' + plot_vis + '_'
    #                                  + str(args["density"])+'.csv')
    # embedded_positions['POS'] = np.array(embedded_positions['POS'].apply(ast.literal_eval))  # need to literal eval
    #
    #
    # # Get original positions
    # original_positions = np.array(df["POS"].tolist())


    # Local quality metric: K-Nearest Neighbors
    fraction_knn = get_knn_quality_metric(original_positions, embedded_positions, k)
    # Global quality metric: Pearson correlation
    pearson_corr, pairwise_data = get_cpd_quality_metric(original_positions, embedded_positions)
    # No ground truth quality metric

    if not align_to_original:
        quality_metrics.update({"K": k, "KNN": fraction_knn, "CPD": pearson_corr})
        # quality_metrics = [k, fraction_knn, pearson_corr]
    else:
        # Compute mean distoriton
        # embedded_positions = np.array(get_position_list(embedded_positions))
        original_distances = pairwise_data[0]  # Pairwise distances in the original space
        embedded_distances = pairwise_data[1]  # Pairwise distances in the reconstructed space
        mean_distortion = align_to_original_image(original_positions, embedded_positions, original_distances,
                                                  embedded_distances)
        quality_metrics.update({"K": k, "KNN": fraction_knn, "CPD": pearson_corr,
                                "Distortion": mean_distortion})


    # KL_loss = compute_KL_divergence(points_original, points_reconstructed)
    # print(f"KL Loss: {KL_loss}")
    print(f"Quality Metrics: {quality_metrics}")
    return quality_metrics


# print(generate_points(100, 10000, dim=2 ))
align_to_original = False
original_pos_file = "posfile_for_weinstein_approach.csv"
# embedded_pos_file = "embedded_pos_weinstein_uei10.csv"
embedded_pos_file = "embedded_pos_weinstein_uei100.csv"
# embedded_pos_file = "embedded_pos_weinstein_try2.csv" # With X transformed (scaled, rotated)

true_index_mapping_file = "true_index_mapping_weinstein_uei100.csv"  # obtained by having my_res copied in matlab
# Preprocess
original_pos = np.delete(np.genfromtxt(original_pos_file, delimiter=','), [0,1], 1)  # delete id and beacon type
embedded_pos = np.delete(np.genfromtxt(embedded_pos_file, delimiter=','), 0, 1)      # delete id
true_index_mapping = np.genfromtxt(true_index_mapping_file, delimiter=',').astype(int)
embedded_pos_target_filtered = np.zeros((10000,2))
for i,row in enumerate(embedded_pos[5000:]):   #4979 for uei10, 5000 for uei100
    #print(true_index_mapping[i])
    embedded_pos_target_filtered[true_index_mapping[i]-1] = row

# find index of all row 0 and delete
# do the same for original pos

delete_this_rows = np.where(np.all(embedded_pos_target_filtered==0, axis=1))
#embedded_pos_target_filtered = embedded_pos_target_filtered[5000:]

original_pos_final_v1 = np.delete(original_pos, delete_this_rows, 0)
embedded_pos_final_v1 = np.delete(embedded_pos_target_filtered, delete_this_rows, 0)


# original_pos = np.genfromtxt(original_pos_file, delimiter=',')   # delete id and beacon type
# embbeded_pos = np.genfromtxt(embedded_pos_file, delimiter=',')      # delete id
# embedded_beacon = embbeded_pos[:4979]
# embedded_target = embbeded_pos[4979:]
# set5000 = set(np.arange(5000).tolist())
# set_beacon = set(embedded_beacon[:,0].tolist())
# set_target = set(embedded_target[:,0].tolist())
# # Indices of discarded UMI
# missing_beacon = set5000.difference(set_beacon)
# missing_target = set5000.difference(set_target)
# missing_target_orig_ind = set([i+5000 for i in list(missing_target)])
#
# original_pos_corrected = np.delete(original_pos, [list(missing_beacon)+list(missing_target_orig_ind)], 0)
# embedded_beacon_ordered = embedded_beacon[embedded_beacon[:, 0].argsort()]
# embedded_target_ordered = embedded_target[embedded_target[:, 0].argsort()]
# print(original_pos_corrected.shape)
# embedded_pos_preprocessed = np.vstack((embedded_beacon_ordered, embedded_target_ordered))


# # Delete index columns
# original_pos_corrected = np.delete(original_pos_corrected, [0,1], 1)
# embedded_pos_preprocessed = np.delete(embedded_pos_preprocessed, 0, 1)


# Find the deleted beacons and targets (by id)
# Delete them in original position
#index_key = np.genfromtxt(index_key_file, delimiter=',').astype(int)

# print(missing_beacon)
# print(missing_target)
# print(missing_target_orig_ind)
# print(embedded_beacon_ordered.shape)
# print(embedded_target_ordered.shape)
# print(embedded_pos_preprocessed.shape)


#embbeded_pos = embbeded_pos[index_key]

# print(original_pos)
# print(embbeded_pos)
# print(index_key)
# print(embbeded_pos.shape)
# print(original_pos.shape)
# np.set_printoptions(threshold=np.inf)
# print(original_pos_corrected)
# np.savetxt("opos_corr_weinstein.csv", original_pos_corrected, delimiter=",")
# np.savetxt("epos_corr_weinstein.csv", embedded_pos_preprocessed, delimiter=",")
#print(main_function_quality_metrics(original_pos_corrected[4979:], embedded_pos_preprocessed[4979:]))
# print(embedded_pos.shape)
# print(embedded_pos_target_filtered)
# print(embedded_pos_target_filtered.shape)
#print(main_function_quality_metrics(original_pos[5000:], embedded_pos_target_filtered))
# print(len(set(np.arange(5000,10000).tolist()).difference(set(true_index_mapping))))
# print(len(true_index_mapping))
# print(len(set(true_index_mapping)))
true_index_mapping = true_index_mapping.tolist()
# print(set([x for x in true_index_mapping if true_index_mapping.count(x) > 1]))
# print(delete_this_rows)

# Adding aid for distortion:

print(main_function_quality_metrics(original_pos_final_v1, embedded_pos_final_v1, align_to_original=True))
