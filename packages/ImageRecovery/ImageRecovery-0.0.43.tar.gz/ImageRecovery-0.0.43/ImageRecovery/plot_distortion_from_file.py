import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
import os


def read_numpy_array(file_name, mode_3D):
    file = open(file_name, mode='r')
    dim = mode_3D+2
    # read all lines at once
    all_string = file.read()
    all_string = all_string.replace("[", "")
    all_string = all_string.replace("]", "")

    np_array = np.fromstring(all_string, dtype=float, sep=' ')
    np_array = np.reshape(np_array, (int(len(np_array)/dim), dim))
    print("reading done!")
    return np_array
def compute_distortion(euclidean_data, mapped_data):
    points_a, points_b = euclidean_data, mapped_data
    #pairwise_matrix = np.linalg.norm(points_a[:, None, :] - points_b[None, :, :], axis=-1)
    distortion_array = np.apply_along_axis(np.linalg.norm, 1, points_a-points_b)  # Compute distance 1to1 between original and reconstructed points
    mean_distortion = np.mean(distortion_array)
    var_distortion = np.var(distortion_array)
    return mean_distortion, var_distortion, distortion_array
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
        # # # Distortion scalebars
        # scalebar_mean = AnchoredSizeBar(ax.transData,
        #                                 float(mean_distortion), 'mean distortion: %.2f' % mean_distortion,
        #                                 "upper center",
        #                                 pad=0.1,
        #                                 #color=rgba_color_mean,
        #                                 color="k",
        #                                 frameon=False,
        #                                 size_vertical=0.01,
        #                                 bbox_to_anchor=Bbox.from_bounds(0, 0, 1.5, 1),
        #                                 bbox_transform=ax.figure.transFigure
        #                                 )
        #
        # scalebar_max = AnchoredSizeBar(ax.transData,
        #                                max_distortion, 'max distortion: %.2f' % max_distortion, "upper center",
        #                                pad=0.1,
        #                                #color=rgba_color_max,
        #                                color="k",
        #                                frameon=False,
        #                                size_vertical=0.01,
        #                                bbox_to_anchor=Bbox.from_bounds(0, 0, 1.5, 0.95),
        #                                bbox_transform=ax.figure.transFigure
        #                                )
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

        # # # Distortion scalebars
        # scalebar_mean = AnchoredSizeBar(ax.transData,
        #                                 float(mean_distortion*typical_length), 'mean distortion: %.2f' % mean_distortion,
        #                                 "upper left",
        #                                 pad=0.1,
        #                                 color = "k", #color=rgba_color_mean,
        #                                 frameon=False,
        #                                 size_vertical=bar_height,
        #                                 bbox_to_anchor=Bbox.from_bounds(0, 0, 0, 1),
        #                                 bbox_transform=ax.figure.transFigure
        #                                 )
        #
        # scalebar_max = AnchoredSizeBar(ax.transData,
        #                                max_distortion*typical_length, 'max distortion: %.2f' % max_distortion, "upper left",
        #                                pad=0.1,
        #                                color="k", #color=rgba_color_max,
        #                                frameon=False,
        #                                size_vertical=bar_height,
        #                                bbox_to_anchor=Bbox.from_bounds(0, 0, 0, 0.95),
        #                                bbox_transform=ax.figure.transFigure
        #                                )
        #
        # scalebar_length = AnchoredSizeBar(ax.transData,
        #                                   1*typical_length, 'cube length %.2f' % 1, "upper left",
        #                                   pad=0.1,
        #                                   color="k", # color=rgba_color_max,
        #                                   frameon=False,
        #                                   size_vertical=bar_height,
        #                                   bbox_to_anchor=Bbox.from_bounds(0, 0, 0, 0.9),
        #                                   bbox_transform=ax.figure.transFigure
        #                                   )
        # ax.add_artist(scalebar_length)
    else:
        raise ValueError('Vectors should be 2 or 3-dimensional')



    # plotet = ax.scatter(mapped_points_positions[:, 0], mapped_points_positions[:, 1], c=distortion_array, cmap="Oranges")
    #plt.colorbar(plotet)






    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm)
    cbar.ax.set_ylabel('distortion')

    # # # Distortion scalebars
    # ax.add_artist(scalebar_mean)
    # ax.add_artist(scalebar_max)

    parent_dir = os.getcwd()
    data_dir = f"{parent_dir}/Output_Documents/Distortion_Plot/Distortion_plots_fig3"
    emb_mode = args["embedding_mode"]
    man_mode = args["manifold_learning_mode"]
    emb_dim = args["embedded_dim"]
    plt.title(f"N = {n_points}\n mean distortion = {round(mean_distortion, 3)}")

    plt.savefig(f"{data_dir}/{emb_mode}_{man_mode}_N={n_points}_dim={dim}_emb_dim={emb_dim}_distortion_line.pdf")
    plt.savefig(f"{data_dir}/{emb_mode}_{man_mode}_N={n_points}_dim={dim}_emb_dim={emb_dim}_distortion_line.png", ppi=600)
    plt.show()



def plot_all_dist_lines_fig3():

    parent_dir = os.getcwd()
    data_dir = f"{parent_dir}/Output_Documents/Distortion_Plot/Distortion_plots_fig3"

    args = {}
    args["embedding_mode"] = "node2vec"
    args["manifold_learning_mode"] = "UMAP"
    args["embedded_dim"] = 32
    # For instructions dict
    density_list = np.linspace(1000, 100000, num=5, dtype=int)
    mode_3D_list = [False, True]

    for density in density_list:
        for mode_3D in mode_3D_list:
            args["density"] = density
            args["mode_3D"] = mode_3D
            original_pos_file = f"{data_dir}/original_pos_N={density}dim={mode_3D+2}.csv"
            mapped_pos_file = f"{data_dir}/mapped_pos_N={density}dim={mode_3D+2}.csv"
            original_pos = read_numpy_array(original_pos_file, mode_3D)
            mapped_pos = read_numpy_array(mapped_pos_file, mode_3D)
            mean_distortion, var_distortion, distortion_array = compute_distortion(original_pos, mapped_pos)
            plot_distortion_lines(original_pos, mapped_pos, distortion_array, args)
# # Run
# plot_all_dist_lines_fig3()