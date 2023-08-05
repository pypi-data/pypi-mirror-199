# Python
import itertools
import time
import tracemalloc
import sys
import logging

# Plots
from matplotlib import colors
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap

# Graph embedding
import csrgraph as cg
import nodevectors  # Gensim version 3.7.1 works properly
import scipy.sparse as sp # sparse arrays
import networkx as nx

# Dimensionality reduction
from sklearn.decomposition import PCA
from sklearn import manifold
import umap

# Our work, helper files
from .reconstruction_colorlabel_and_plots import *  # Assists in coloring reconstructions
from .quality_metrics import *  # Computes proximity graphs and accuracy scores



def read_node_label(filename, skip_head=False):
    fin = open(filename, 'r')
    X = []
    Y = []
    while 1:
        if skip_head:
            fin.readline()
        l = fin.readline()
        if l == '':
            break
        vec = l.strip().split(' ')
        X.append(vec[0])
        Y.append(vec[1:])
    fin.close()
    return X, Y


def write_embedded_position(u, n_components, directory, embedding_mode, dim_red, shape_str):
    numb_nodes = str(shape_str[0])
    if n_components == 2:
        positions = list(zip(u[:, 0], u[:, 1]))  # x, y
    else:
        positions = list(zip(u[:, 0], u[:, 1], u[:, 2]))  # x, y, z
    # Write document for posterior processing
    f = open(directory + '/Output_Documents/Embedded_Positions/embedded_pos_' +
             embedding_mode + "_" + dim_red + "_" + numb_nodes + '.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['POS'])
    for i in range(len(u[:, 0])):
        writer.writerow([positions[i]])
    f.close()


def write_lowD_vectors(vectors, directory, embedding_mode, shape_str):
    length_nodes, low_D = shape_str
    path_to_file = directory + "/Output_Documents/Embedded_Vectors/" \
                               "embedded_vectors" + "_" + embedding_mode + "_" + str(length_nodes) + ".csv"
    np.savetxt(path_to_file,
               vectors, delimiter=" ",
               header=f"{length_nodes} {low_D}",
               comments='')


def _square_lim(lim_low, lim_high):
    if abs(lim_low) > abs(lim_high) and lim_low < 0:
        return (lim_low, -lim_low)
    elif abs(lim_low) <= abs(lim_high) and lim_high > 0:
        return (-lim_high, lim_high)
    else:
        return (lim_low, lim_high)


def plot_umap_control_embedded(self, data, start_time, args, n_neighbors=15, min_dist=1, n_components=2,
                               metric='euclidean', title='',
                               densmap=False, embedding_mode="node2vec", embedded_dim=32,
                               shape_str="(1000,64)"):
    """""

    """""
    if self.mode_3D:
        n_components = 3
    if self.color_grid == "tri_checkers":
        total_colors = 3
        color_map = colors.ListedColormap(['b', 'r', 'g'])
    elif self.color_grid == "swedish_flag":
        total_colors = 2
        color_map = colors.ListedColormap(['b', 'y'])
    elif self.color_grid == "pixel_monster":
        total_colors = 2
        color_map = colors.ListedColormap(['#e6ede6', 'k'])
    elif self.color_grid == "triangle":
        total_colors = 2
        color_map = colors.ListedColormap(['b', 'k'])
    elif self.color_grid == "distortion":
        total_colors = 2
        color_map = colors.ListedColormap(['#FF1F58', '#009ADE'])
        if self.mode_3D == True:
            total_colors = 3
            color_map = colors.ListedColormap(['#FF1F58', '#009ADE', '#f00'])
    elif self.color_grid == "hue":
        # color_map = "viridis"
        total_colors = 16
        cmap = cm.get_cmap('Oranges', 15)  # PiYG
        color_map = []
        for i in range(cmap.N):
            rgba = cmap(i)
            color_map.append(matplotlib.colors.rgb2hex(rgba))
        color_map.append("#f00")
        color_map = colors.ListedColormap(color_map, N=total_colors)
    elif self.color_grid == "concentric":
        color_map = []


    elif self.color_grid == "gaussian":
        color_map = []

    else:
        # Mario colormap
        total_colors = 11
        color_map = colors.ListedColormap([
            '#f00',
            '#fff',
            '#000',
            '#55ede3',  # --> 1
            '#83401f',
            '#ffbc77',
            '#06f',
            '#ff0',
            '#ff8000',
            '#5ac528',
            '#FF000000'], N=total_colors)

    vectors = data

    shape = list(np.shape(vectors))
    if shape[1] < 5:
        shape[1] = embedded_dim  # Please input the low dimension you want to plot: 2D or 3D

    if self.args["embedding_mode"] == "node2vec" and self.dim_reduction_vis != "directly":
        shape[1] = embedded_dim

    if self.args["proximity_mode"] != "experimental":
        X, Y = read_node_label(self.current_dir + "/Input_Documents/Label_Lists/"
                               + "label_list_" + embedding_mode + "_" + \
                               str(shape_str) + ".csv")  # X: node, Y: label
        # Each label is a color
        color_list = [int(label[0]) for label in Y]
    else:
        color_list = [1 for _ in range(np.shape(vectors)[0])]

    if (embedding_mode == "node2vec") and self.dim_reduction_vis != "directly":

        emb_list = []
        dict_data = {}
        for (index, vector) in enumerate(vectors):
            dict_data[int(vector[0])] = np.array([vector[i] for i in range(1, len(vector))])

        for k in range(1, len(vectors) + 1):
            if int(k) in dict_data:
                emb_list.append(dict_data[int(k)])  # high-D vectors list

        emb_list = np.array(emb_list)

    else:
        emb_list = data  # matrix NxD

    write_lowD_vectors(emb_list, self.current_dir, embedding_mode, shape_str)
    print("shape embedded vectors:", np.shape(emb_list))

    if self.dim_reduction_vis == "UMAP":
        fit = umap.UMAP(
            n_neighbors=n_neighbors,
            min_dist=min_dist,
            n_components=n_components,
            metric=metric,
            densmap=densmap,
        )
        u = fit.fit_transform(emb_list)

    elif self.dim_reduction_vis == 'PCA':
        pca = PCA(n_components=n_components)
        u = pca.fit_transform(emb_list)

    elif self.dim_reduction_vis == "directly":
        if np.shape(emb_list)[1] != n_components:
            print("ERROR: Embedding must be in 2D or 3D")
        u = emb_list

    elif self.dim_reduction_vis == "original_image":
        if np.shape(emb_list)[1] != n_components:
            print("ERROR: Embedding must be in 2D or 3D")
        u = emb_list
    print("Dimensionality reduction done --- %s seconds  ---" % (time.time() - start_time))

    total_time_iteration = time.time() - start_time
    peak_memory = tracemalloc.get_traced_memory()[1]
    peak_memory_mb = peak_memory / (1024 ** 2)
    tracemalloc.stop()
    print(f"Peak memory --- {peak_memory_mb} MB")

    # Store the embedded positions
    write_embedded_position(u, n_components, self.current_dir, self.args["embedding_mode"], self.dim_reduction_vis,
                            shape_str)

    # COMPUTE QUALITY METRICS --> Returns K, KNN, CPD and distortion (if align = true)
    quality_metrics = main_function_quality_metrics(args, self.neighbor_dataframe, self.current_dir,
                                                    embedding_mode, self.dim_reduction_vis, self.args["proximity_mode"],
                                                    k=self.args["n_neighbors"], radius=self.args["radius"],
                                                    align_to_original=self.args["align_to_original"])
    # --------------------------------------------------------------------------
    # PLOTTING
    # --------------------------------------------------------------------------
    if self.plot_mode:
        norm = colors.Normalize(vmin=np.amin(color_list), vmax=np.amax(color_list))
        rgba_list = []
        for color in color_list:
            if color == -1:
                rgba = np.array([0, 0, 0, 0]) * 255  # Transparent color
            else:
                rgba = np.array(cm.coolwarm(norm(color))) * 255
            rgba_list.append(rgba)
        rgba_list = np.array(rgba_list)

        if self.args["proximity_mode"] == "experimental":  # TODO We don't have color labels for experimental results
            color_list = np.full(len(u[:, 0]), 0)

        fig = plt.figure(figsize=(6, 6))

        if n_components == 2:
            if self.color_grid == "concentric_faces":
                color_list = rgba_list / 255
                ax = fig.add_subplot(111)
                ax.scatter(u[:, 0], u[:, 1], c=color_list, marker=".", s=5)
                ax.set_xlabel('x axis (arbitrary units)')
                ax.set_ylabel('y axis (arbitrary units)')
                prox_mode = self.args["proximity_mode"]
                plt.savefig(self.current_dir + f'/Reconstructed_Figures/recons_image_dim={n_components}D_'
                                               f'size_and_embdim={shape_str}_embedding_mode={self.embedding_mode}_'
                                               f'manifold_mode={self.dim_reduction_vis}_colorgrid={self.color_grid}_'
                                               f'_neighbors={str(n_neighbors)}_prox_mode={prox_mode}.pdf')

            else:
                ax = fig.add_subplot(111)
                ax.scatter(u[:, 0], u[:, 1], c=color_list, cmap=color_map, vmin=0, vmax=total_colors, marker=".", s=5)
                ax.set_xlabel('x axis (arbitrary units)')
                prox_mode = self.args["proximity_mode"]
                plt.savefig(self.current_dir + f'/Reconstructed_Figures/recons_image_dim={n_components}D_'
                                               f'size_and_embdim={shape_str}_embedding_mode={self.embedding_mode}_'
                                               f'manifold_mode={self.dim_reduction_vis}_colorgrid={self.color_grid}_'
                                               f'_neighbors={str(n_neighbors)}_prox_mode={prox_mode}.pdf')
            # plt.show()
            # plt.close(fig)
        if n_components == 3:
            # FANCY PLOTTING WITH SHADOWS (2D): ax1, fig
            # 3D animation: ax, fig2
            # Heatmap quality metrics: ax3, fig3
            x, y, z = u[:, 0], u[:, 1], u[:, 2]

            color_list = np.array(color_list)
            norm = colors.Normalize(vmin=np.amin(color_list), vmax=np.amax(color_list))
            rgba_list = []
            for color in color_list:
                if color == -1:
                    rgba = np.array([0, 0, 0, 0]) * 255  # Transparent color
                else:
                    rgba = np.array(cm.coolwarm(norm(color))) * 255
                rgba_list.append(rgba)
            rgba_list = np.array(rgba_list)

            # 3D plot
            ax1 = Axes3D(fig, auto_add_to_figure=False)  # auto_add_to_figure=False, fig.add_axes(ax)
            fig.add_axes(ax1)
            if self.color_grid == "concentric_faces":
                color_list = rgba_list / 255
                im = ax1.scatter(
                    x,
                    y,
                    z,
                    c=color_list
                )
                azimut = 45
                plt.axis("off")
                ax1.view_init(elev=45, azim=azimut)
                plt.savefig(self.current_dir + f"/Reconstructed_Figures/" + "azimut%d.jpeg" % azimut, dpi=600)

            else:
                im = ax1.scatter(
                    x,
                    y,
                    z,
                    c=color_list,
                    cmap=color_map,
                )
            plt.axis('off')

            prox_mode = self.args["proximity_mode"]
            plt.savefig(self.current_dir + f'/Reconstructed_Figures/recons_image_dim={n_components}D_'
                                           f'size_and_embdim={shape_str}_embedding_mode={self.embedding_mode}_'
                                           f'manifold_mode={self.dim_reduction_vis}_colorgrid={self.color_grid}_'
                                           f'_neighbors={str(n_neighbors)}_prox_mode={prox_mode}.pdf')
            # plt.show()
            #plt.close(fig)
            if self.mode_anim:  # If we want to save animation
                fig2 = plt.figure()
                ax = Axes3D(fig2, auto_add_to_figure=False)  # auto_add_to_figure=False, fig.add_axes(ax)
                fig2.add_axes(ax)
                # 3D animation
                plt.axis('off')

                def init():
                    # Plot the surface.
                    ax.scatter(u[:, 0], u[:, 1], u[:, 2], c=color_list, cmap=color_map, vmin=0, vmax=total_colors)
                    return fig2,

                def animate(i):
                    # # Activate to zoom out
                    # reduction = 3
                    # ax.set_xlim(-i / reduction, i / reduction)
                    # ax.set_ylim(-i / reduction, i / reduction)
                    # ax.set_zlim(-i / reduction, i / reduction)
                    ax.view_init(elev=i * 1, azim=i * 2)
                    return fig,

                # Animate
                ani = animation.FuncAnimation(fig2, animate, init_func=init,
                                              frames=90, interval=10, blit=True)
                fn = self.current_dir + '/Reconstructed_Animations/recons_image_' \
                     + str(shape_str) + "_" + self.embedding_mode + "_" + self.dim_reduction_vis \
                     + "_colors_" + str(self.partition) + "_" + self.proximity_mode

                ani.save(fn + '.gif', writer='imagemagick', fps=1000 / 50)
                print("Animation done --- %s seconds  ---" % (time.time() - start_time))

        plt.gca().set_aspect('auto', adjustable='box')  # for 2d you can set 'equal' instead of 'auto'
        #plt.draw()
        plt.title(title, fontsize=18)

    quality_metrics.update({"Time": total_time_iteration, "Memory": peak_memory_mb})
    print(f"Quality metrics: {quality_metrics}")
    return quality_metrics  # Return KNN, CPD, Time, DIS, Memory, NGT KNN


# INITIALIZE
# --------------------------------------------------------------


def create_folder_if_not_exist(parent_dir, folder_name):
    path = parent_dir + "/" + folder_name
    isExist = os.path.exists(path)
    # Check whether the specified path exists or not
    if not isExist:
        # Create a new directory because it does not exist
        os.makedirs(path)
        print(f"The new directory {path} is created!")


def create_folder_structure(parent_dir):
    """" Creates necessary folders to run the code
         folder_structure: dictionary with key = outer_folders, value = list of inner_folders
    """
    folder_structure = {"Computational_Complexity_Plot": [],
                        "Input_Documents": ["Edge_Lists", "Label_Lists", "Positions_And_Neighbors"],
                        "Output_Documents": ["Embedded_Positions", "Embedded_Vectors", "Distortion_Plot"],
                        "Parameter_Analysis": ["Data"],
                        "Reconstructed_Animations": [],
                        "Reconstructed_Figures": [],
                        "Scalability_vs_Metrics_Plot": [],
                        "Appendix_Data": []
                        }

    # Create folders if they don't exist
    for (k, v) in folder_structure.items():
        create_folder_if_not_exist(parent_dir, k)
        subparent_dir = parent_dir + "/" + k
        for child_dir in v:
            create_folder_if_not_exist(subparent_dir, child_dir)


class MainParameters:
    def __init__(self, args):
        self.args = args

    def choose_beta_or_weibull(self, desired_degree, epsilon_range, N):
        x = np.linspace(0, 1, 1000)  # 1000 as space partition
        if self.args["proximity_mode"] == "beta_multimodal":
            a1, a2 = 5, 5
            mode1, mode2 = 0.3, 0.9  # In a 0,1 interval
            b1, b2 = get_beta_given_mode(a1, mode1), get_beta_given_mode(a2, mode2)
            prox_parameters = (a1, a2, b1, b2)
            epsilon, scale_x, scale_y, composition = get_pdf_parameters_desired_degree_beta_multimodal(desired_degree,
                                                                                                       epsilon_range, N,
                                                                                                       x, a1, b1, a2,
                                                                                                       b2, self.args[
                                                                                                           "mode_3D"])
        elif self.args["proximity_mode"] == "weibull_decaying_1":
            parameter_k = 1
            parameter_lambda = 1
            prox_parameters = (parameter_k, parameter_lambda)
            epsilon, scale_x, scale_y, composition = get_pdf_parameters_desired_degree_weibull(desired_degree,
                                                                                               epsilon_range, N, x,
                                                                                               parameter_k,
                                                                                               parameter_lambda,
                                                                                               self.args["mode_3D"])
        elif self.args["proximity_mode"] == "weibull_2":
            parameter_k = 1.5
            parameter_lambda = 0.5
            prox_parameters = (parameter_k, parameter_lambda)
            epsilon, scale_x, scale_y, composition = get_pdf_parameters_desired_degree_weibull(desired_degree,
                                                                                               epsilon_range, N, x,
                                                                                               parameter_k,
                                                                                               parameter_lambda,
                                                                                               self.args["mode_3D"])
        elif self.args["proximity_mode"] == "weibull_3":
            parameter_k = 10
            parameter_lambda = 0.5
            prox_parameters = (parameter_k, parameter_lambda)
            epsilon, scale_x, scale_y, composition = get_pdf_parameters_desired_degree_weibull(desired_degree,
                                                                                               epsilon_range, N, x,
                                                                                               parameter_k,
                                                                                               parameter_lambda,
                                                                                               self.args["mode_3D"])
        else:
            return 0, 0, 0, (0, 0)
        print(f"radius: {epsilon}, scale_x: {scale_x}, scale_y: {scale_y}, prox_parameters: {prox_parameters}")
        return epsilon, scale_x, scale_y, prox_parameters

    def node_embedding_manifold_learning_main(self):
        # PREPROCESSING
        current_dir = os.getcwd()
        numb_nodes = int(
            self.args["L"] ** (self.args["mode_3D"] + 2) * self.args[
                "density"])  # To the power of 3 in 3D, to the power of 2 in 2D * density
        if self.args["proximity_mode"] == "experimental":
            self.args["generate_new_knn_data"] = False
        if self.args["generate_new_knn_data"]:
            # Here the proximity graph is generated
            epsilon, scale_x, scale_y, prox_parameters = self.choose_beta_or_weibull(self.args["n_neighbors_knn"],
                                                                                     self.args["radius_range"],
                                                                                     self.args["density"])
            if epsilon != 0:
                self.args["radius"] = epsilon
            # Generate proximity graph and write its edges
            write_positions_and_knn(self.args["L"], numb_nodes, current_dir, k=self.args["n_neighbors_knn"],
                                    radius=self.args["radius"], proximity_mode=self.args["proximity_mode"],
                                    mode_3D=self.args["mode_3D"],
                                    weighting=self.args["weighting"],
                                    scale_x=scale_x, scale_y=scale_y, prox_parameters=prox_parameters)
            if self.args["embedding_mode"] == "node2vec":
                node2vec_parameters = self.args["node2vec_parameters"]   # use node2vec parameters
                doc_title = current_dir + "/Input_Documents/Positions_And_Neighbors/neighbors_data_" + str(
                    int(self.args["mode_3D"] + 2)) + "D_" \
                            + str(numb_nodes) + "_" + "knn" + ".csv"
            else:
                doc_title = current_dir + "/Input_Documents/Positions_And_Neighbors/neighbors_data_" + str(
                    int(self.args["mode_3D"] + 2)) + "D_" \
                            + str(numb_nodes) + "_" + self.args[
                                "proximity_mode"] + ".csv"  # document containing position and neighbor information
            df = pd.read_csv(doc_title)
            df = apply_literal_format_to_df(df)  # convert string to int
        else:
            df = pd.DataFrame()  # empty dataframe when data is not generated
        if self.args["proximity_mode"] == "experimental":
            title_edge_list = current_dir + "/Input_Documents/Edge_Lists/" + self.args["title_edge_list_experimental"]
        else:
            title_edge_list = current_dir + "/Input_Documents/Edge_Lists/edge_list_" + self.args[
                "proximity_mode"] + "_" + str(self.args["density"]) + ".csv"
        self.args["title_edge_list"] = title_edge_list
        # /home/david/PycharmProjects/Node_Embedding_Python/Input_Documents/Edge_Lists/edge_list_shortest_paths_(1000, 32).csv
        title_label_list = current_dir + "/Input_Documents/Label_Lists/label_list_" + self.args[
            "embedding_mode"] + "_" + \
                           str((numb_nodes, self.args["embedded_dim"])) + ".csv"
        shape_str = (numb_nodes, self.args["embedded_dim"])  # tuple with nodes and dim, useful for titling the files

        # PARAMETERS: L, self.args["partition"], self.args["mode_3D"],, mode_anim, color_grid, dataframe
        # --------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------
        # Enforcing some conditions:
        if (self.args["embedding_mode"] == "landmark_isomap") or self.args["embedding_mode"] == "spring_relaxation":
            emb_mode = self.args["embedding_mode"]
            print(f"Enforcing to not use manifold learning for {emb_mode}")
            self.args["manifold_learning_mode"] = "directly"  # Use Multidimensional Scaling for Landmark Isomap
        if (self.args["mode_3D"] == True) and (
                self.args["density"] < 100000):  # concentric faces needs many points (resolution)
            self.args["pixel_art"], pixel_art = "tri_checkers", "tri_checkers"
            self.args["partition"], partition = 3, 3



        parameters = PlotParameters(self.args["L"], self.args["partition"], self.args["mode_3D"],
                                    self.args["mode_anim"], self.args["pixel_art"], df,
                                    self.args["manifold_learning_mode"], current_dir, self.args["embedding_mode"],
                                    self.args["weighting"],
                                    self.args["node2vec_parameters"], self.args["proximity_mode"],
                                    self.args["plot_mode"], self.args)

        # --------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------

        PlotParameters.plot_umap_control_embedded = plot_umap_control_embedded  # turn into method

        # Write edges to create graph!!! If graph data is synthetic
        if self.args["generate_new_knn_data"]:
            color_list = parameters.get_labels_by_position(title_label_list)  # assign labels to each point
            parameters.get_edge_list(title_edge_list,
                                     weighting=self.args[
                                         "weighting"])  # write edges. choose if graph is weighted (and what weights)
            self.args["title_edge_list"] = title_edge_list

        # Read Graph
        if self.args["weighting"] == "unweight":
            nx_graph = nx.read_edgelist(title_edge_list,
                                        delimiter=self.args["exp_delimiter"])  # Original graph, change delimiter accordingly: normally " ", sometimes ","
        else:  # weighted case
            nx_graph = nx.read_edgelist(title_edge_list, delimiter=self.args["exp_delimiter"], nodetype=int,
                                        data=(("weight", float),))

        is_connected = nx.is_connected(nx_graph)
        self.args["is_connected"] = is_connected
        if not is_connected:
            raise ValueError(
                "The edge list provided results in an unconnected graph. Please provide either a connected "
                "or a connected subgraph")
        else:
            G = cg.read_edgelist(title_edge_list, directed=False, sep=' ')

        time_preprocess = time.time() - self.args["start_time"]
        print("PreProcessing done --- %s seconds  ---" % time_preprocess)
        self.args["start_time"] = time.time()  # Reset start time

        # Check if we read from embedded positions from file
        if not self.args["generate_dim_reduction"]:
            path_to_file = current_dir + "/Output_Documents/Embedded_Positions/" \
                                         "embedded_pos" + "_" + self.args["embedding_mode"] + "_" + \
                           self.args["manifold_learning_mode"] + "_" + str(
                numb_nodes) + ".csv"
            if self.args["embedding_mode"] == "original_image":
                path_to_file = current_dir + "/Input_Documents/Positions_And_Neighbors/" \
                                             "neighbors_data" + "_" + str(self.args["mode_3D"] + 2) + "D_" + str(
                    numb_nodes) + "_" + self.args["proximity_mode"] + ".csv"

            print("accessing info from", path_to_file)
            if not os.path.exists(path_to_file):
                raise ValueError(f"ERROR: FILE DOES NOT EXIST. \nFix by setting generate_dim_reduction "
                                 f"= True or setting a different embedding mode."
                                 f"\nCurrent file trying to be accessed: {path_to_file}")

            else:
                u = pd.read_csv(path_to_file, converters={0: ast.literal_eval})
                u = np.array([*u.POS])
                vectors = u  # NumPy array



        elif not self.args["generate_embedding_vectors"]:
            path_to_file = current_dir + "/Output_Documents/Embedded_Vectors/" \
                                         "embedded_vectors" + "_" + self.args["embedding_mode"] + "_" + str(
                numb_nodes) + ".csv"

            if not os.path.exists(path_to_file):
                raise ValueError(f"ERROR: FILE DOES NOT EXIST. \nFix by setting generate_embedding_vectors "
                                 f"= True or setting a different embedding mode."
                                 f"\nCurrent file trying to be accessed: {path_to_file}")
            else:
                u = pd.read_csv(path_to_file, sep=" ", header=None, skiprows=1)
                u = u.astype(float)  # From string to float
                vectors = np.array(u)  # NumPy array

        # If not reading from already created "embedded vectors" file, create a new embedding
        else:
            if self.args["embedding_mode"] == "node2vec":
                g2v = nodevectors.Node2Vec(
                    n_components=self.args["embedded_dim"],
                    walklen=self.args["walklen"],
                    return_weight=self.args["return_weight"],  # Setting this high: BFS
                    neighbor_weight=self.args["neighbor_weight"]  # Setting this high: DFS
                )
                g2v.fit(G)
                g2v.save_vectors("Output_Documents/Embedded_Vectors/node2vec_embedded_vectors.csv")
                u = pd.read_csv("Output_Documents/Embedded_Vectors/node2vec_embedded_vectors.csv", sep=" ", header=None,
                                skiprows=1)
                u = u.astype(float)
                vectors = np.array(u)
                print(f"{np.shape(vectors)}")

            elif self.args["embedding_mode"] == "ggvec":
                # Careful with number of components. Too high produces weird
                # Negatie ratio [0,1], the higher, the slower and more quality
                # Exponent gives importance to higher weighted edges
                ggvec_model = nodevectors.GGVec(n_components=self.args["embedded_dim"], negative_ratio=1, exponent=1)
                vectors = ggvec_model.fit_transform(G)


            elif self.args["embedding_mode"] == "landmark_isomap":
                # Compute shortest paths from the edge_list
                adjacency_matrix = from_edge_list_to_adjacency_matrix(title_edge_list)
                distance_matrix = sp.csgraph.shortest_path(adjacency_matrix, directed=False)
                # Select random landmarks
                selected_landmarks = np.random.choice(np.arange(self.args["density"]), self.args["embedded_dim"], replace=False)
                # Select distance from every node to every landmark (NxD matrix)
                all_distances_to_landmarks = np.array(distance_matrix[:, selected_landmarks])
                # Landmark DxD distance matrix (symmetric positive)
                landmark_distance_matrix = all_distances_to_landmarks[selected_landmarks]

                def landmark_MDS(diss_matrix_landmarks, all_distance_to_landmarks):
                    """
                    1. Apply MDS to position landmark nodes
                    2. Use landmark positions eigenvalues (moore penrose inverse) to position the rest of the nodes
                    """
                    mds = manifold.MDS(n_components=self.args["mode_3D"] + 2, metric=True, random_state=2,
                                       dissimilarity="precomputed")
                    L = np.array(mds.fit_transform(diss_matrix_landmarks))  # landmark_coordinates --> good results

                    # Triangulate all points
                    D2 = diss_matrix_landmarks ** 2
                    D2_all = all_distance_to_landmarks ** 2
                    mean_column = D2.mean(axis=0)
                    L_slash = np.linalg.pinv(L)
                    recovered_positions = np.transpose(0.5 * L_slash.dot(np.transpose(mean_column - D2_all)))
                    return recovered_positions

                recovered_positions = landmark_MDS(landmark_distance_matrix, all_distances_to_landmarks)
                vectors = recovered_positions
                print("shape positions", np.shape(vectors))

            elif self.args["embedding_mode"] == "spring_relaxation":
                pos_array = np.empty((self.args["density"], self.args["mode_3D"] + 2))
                pos_dic = nx.spring_layout(nx_graph, dim=self.args["mode_3D"] + 2,
                                           iterations=500)  # Fruchteman-Reingold algo
                for k, v in pos_dic.items():
                    pos_array[int(k) - 1] = v  # k-1 because node index start at 1
                vectors = pos_array


            elif self.args["embedding_mode"] == "shortest_paths":
                # Compute shortest paths from the edge_list
                adjacency_matrix = from_edge_list_to_adjacency_matrix(title_edge_list)
                distance_matrix = sp.csgraph.shortest_path(adjacency_matrix, directed=False)
                print("distance matrix computed")
                distance_matrix = np.array(distance_matrix)
                vectors = distance_matrix

            elif self.args["embedding_mode"] == "original_image":
                vectors = np.array(list(df['POS']))

        time_embedding = time.time() - self.args["start_time"]
        print("Embedding done --- %s seconds  ---" % time_embedding)

        # scaler = preprocessing.StandardScaler()
        # scaler = preprocessing.MinMaxScaler()

        # vectors = scaler.fit_transform(vectors)                    # standardize /minmax   cpd 0.61 and knn 0.23 as opposed to 0.56 and 0.26 with no standardization
        # vectors = preprocessing.normalize(vectors, norm='l2')     # normalize

        # Particular case where we use already known embedded positions
        if self.args["generate_dim_reduction"] == False:
            parameters.dim_reduction_vis = "directly"

        quality_metrics_dict = parameters.plot_umap_control_embedded(data=vectors, start_time=self.args["start_time"],
                                                                     args=self.args, min_dist=1,
                                                                     n_neighbors=self.args["n_neighbors"],
                                                                     densmap=False,
                                                                     embedding_mode=self.args["embedding_mode"],
                                                                     embedded_dim=self.args["embedded_dim"],
                                                                     shape_str=shape_str)
        return quality_metrics_dict


def from_edge_list_to_adjacency_matrix(title_edge_list):
    edge_list = pd.read_csv(title_edge_list, names=["source", "sink"], header=None, delimiter=" ")  # Read
    N = max(edge_list["source"])  # number of nodes
    # Define row, col, data (i,j and weight value of the adj matrix)
    row = np.array(edge_list["source"] - 1)  # substract 1 so we start at 0
    col = np.array(edge_list["sink"] - 1)
    data = np.empty(len(edge_list))
    data.fill(1)  # Fill it with edge weight values, for undirected all weights = 1

    adjacency_matrix = sp.csr_matrix((data, (row, col)), shape=(N, N)).toarray()
    return adjacency_matrix

def recover_image_try_different_seeds(default_params):
    count = 0
    while True:
        try:
            tracemalloc.start()
            main_parameters = MainParameters(default_params)  # Establish parameters
            quality_metrics_dict = main_parameters.node_embedding_manifold_learning_main()  # Call main function
            tracemalloc.stop()
            if count > 10:  # If after 10 iterations a connected graph is not generated, break
                break
        except:
            pass
        else:
            break
    return quality_metrics_dict

def iterate_main(variable_params, default_params):
    """""
    Iterate a function over *some* of its arguments.
     
    INPUT:
        variable_params - dictionary of arguments to iterate over 
        default_params  - dictionary containing *all* arguments
        
        Example of variable_params:
            number_samples = 6
            embedded_dim_list = np.array([4, 16, 32, 128, 512, 2048])
            n_neighbors_list = np.array([4, 16, 32, 128, 512, 2048])
            return_weight_list = np.logspace(np.log10(0.1), np.log10(10), num=number_samples)
            neighbor_weight_list = np.logspace(np.log10(0.1), np.log10(10), num=number_samples)
            walklen_list = np.logspace(np.log10(3), np.log10(100), num=number_samples).astype(int)

            variable_params = {
                "embedded_dim": embedded_dim_list,
                # "density" : density_list,
                "n_neighbors": n_neighbors_list,
                "return_weight": return_weight_list,
                "neighbor_weight": neighbor_weight_list,
                "walklen": walklen_list
            }
    OUTPUT:
        CSV file containing accuracy and computational complexity for each argument variation
        Can be found in /Parameter_Analysis/Data/ folder.
    """""

    default_params["align_to_original"] = True # Assert distortion computation
    for key in variable_params:
        list_data = []
        default_auxiliary = copy.copy(default_params)
        print("DEFAULT AUXILIARY: SHOULD REMAIN THE SAME!", default_auxiliary)
        # Iterate over all possible parameter values
        for i, param in enumerate(variable_params[key]):
            start_time = time.time()
            default_auxiliary["start_time"] = start_time
            default_auxiliary[key] = param
            main_parameters = MainParameters(default_auxiliary)  # Establish parameters
            tracemalloc.start()
            quality_metrics_dict = main_parameters.node_embedding_manifold_learning_main()  # Call main function
            quality_metrics_old_list = [param, quality_metrics_dict["KNN"],
                                        quality_metrics_dict["CPD"], quality_metrics_dict["Distortion"],
                                        quality_metrics_dict["Time"], quality_metrics_dict["Memory"]]
            tracemalloc.stop()
            if i == 0:  # Repeat first iteration to avoid "precomputation time"
                start_time = time.time()
                default_auxiliary["start_time"] = start_time
                default_auxiliary[key] = param
                main_parameters = MainParameters(default_auxiliary)  # Establish parameters
                tracemalloc.start()
                quality_metrics_dict = main_parameters.node_embedding_manifold_learning_main()  # Call main function
                quality_metrics_old_list = [param, quality_metrics_dict["KNN"],
                                            quality_metrics_dict["CPD"], quality_metrics_dict["Distortion"],
                                            quality_metrics_dict["Time"], quality_metrics_dict["Memory"]]
                tracemalloc.stop()
            list_data.append(quality_metrics_old_list)
        # Input data into a dataframe and write it
        parameters_df = pd.DataFrame(list_data, columns=[key, "KNN", "CPD", "Distortion", "Time", "Memory"])
        parameters_df.to_csv(f'Parameter_Analysis/Data/{key}_data.csv')


def iterate_proximity_graphs_utility(default_params, density_list, proximity_mode_list):
    """
    Input
        default params: image recovery parameters

        density_list: set of density values, e.g.     density_list = np.linspace(1000, 100000, num=5)

        proximity_mode_list: set of proximity modes to iterate, e.g.
            proximity_mode_list = ["knn", "epsilon-ball", "delaunay", "beta_multimodal", "weibull_decaying_1", "weibull_2",
                       "weibull_3", "knn_weighted"]
    Output
        CSV file for each proximity mode containing accuracy / system size
        Can be found in folder "/Scalability_vs_Metrics_Plot/"
    """
    if not default_params["align_to_original"]:
        raise ValueError("align_to_original not activated, can't compute distortion! Please set align_to_original=True")

    # density_list = np.linspace(1000, 100000, num=5)
    # density_list = np.logspace(np.log10(1000), np.log10(100000), num=5)
    for proximity_mode in proximity_mode_list:
        print(proximity_mode)
        default_params["proximity_mode"] = proximity_mode
        if proximity_mode == "knn_weighted":
            default_params["weighting"] = "inverse_distance"
        pre_quality_df = []  # Will append row values to this list, afterwards it will be transformed into a dataframe
        for density in density_list:
            density = int(density)
            default_params["density"] = density

            # # Uncomment for 1 trial only
            # main_parameters = MainParameters(default_params)
            # print("done")
            # tracemalloc.start()
            # quality_metrics_dict = main_parameters.node_embedding_manifold_learning_main()  # add distortion parameter!
            # metrics_dict = {"N": density,
            #                 "KNN": quality_metrics_dict["KNN"],
            #                 "CPD": quality_metrics_dict["CPD"],
            #                 "Time": quality_metrics_dict["Time"],
            #                 "Distortion": quality_metrics_dict["Distortion"],
            #                 "Memory": quality_metrics_dict["Memory"],
            #                 "NGT KNN": quality_metrics_dict["NGT KNN"]}
            # pre_quality_df.append(metrics_dict)

            # Uncomment for more than 1 trial
            count = 0
            while True:
                try:
                    count += 1
                    default_params["density"] = density
                    main_parameters = MainParameters(default_params)
                    quality_metrics_dict = main_parameters.node_embedding_manifold_learning_main()  # add distortion parameter!
                    metrics_dict = {"N": density,
                                    "KNN": quality_metrics_dict["KNN"],
                                    "CPD": quality_metrics_dict["CPD"],
                                    "Time": quality_metrics_dict["Time"],
                                    "Distortion": quality_metrics_dict["Distortion"]}

                    pre_quality_df.append(metrics_dict)
                    print("error count", count)
                except Exception as e:
                    logging.error('Error:' + str(e))
                    if count > 10:  # If after 10 iterations a connected graph is not generated, break
                        print("error count", count)
                        break
                    pass
                else:
                    break
        proximity_mode_dataframe = pd.DataFrame(pre_quality_df)
        df_path = os.getcwd() + "/Scalability_vs_Metrics_Plot/"

        # Shorter names
        dim = default_params["mode_3D"] + 2
        # df_delaunay_dim=2_okt2722
        proximity_mode_dataframe.to_csv(df_path + f"df_{proximity_mode}_dim={dim}_dec22.csv", sep='\t')


def iterate_several_instructions_utility(default_params, instructions_iterator):
    """
    Input
        default params: image recovery parameters

        instructions_iterator:
        iterator containing sets of parameter information. For example, if we want to iterate over 3 proximity graphs
        and output dimension 2D and 3D using node2vec --> 6 sets of parameters

            ({'mode_3D': False}, {'embedding_mode': 'node2vec'}, {'proximity_mode': 'knn'})
            ({'mode_3D': False}, {'embedding_mode': 'node2vec'}, {'proximity_mode': 'delaunay'})
            ({'mode_3D': False}, {'embedding_mode': 'node2vec'}, {'proximity_mode': 'weibull_2'})
            ({'mode_3D': True}, {'embedding_mode': 'node2vec'}, {'proximity_mode': 'knn'})
            ({'mode_3D': True}, {'embedding_mode': 'node2vec'}, {'proximity_mode': 'delaunay'})
            ({'mode_3D': True}, {'embedding_mode': 'node2vec'}, {'proximity_mode': 'weibull_2'})

        to construct such the iterator we need "instructions" and itertools.product, see below:

        mode_3D_instruction = [{"mode_3D": False}, {"mode_3D": True}]
        embedding_mode_instruction = [{"embedding_mode": "node2vec"}]
        proximity_mode_list_instructions = ["knn", "delaunay", "weibull_2"]
        proximity_mode_instruction = [{"proximity_mode": prox_mode} for prox_mode in proximity_mode_list_instructions]
        embedding_mode_instruction = [{"embedding_mode": "node2vec"}]
        --> instructions_iterator = itertools.product(mode_3D_instruction, embedding_mode_instruction, proximity_mode_instruction)


        # Iterate instructions used #
        proximity_mode_list_instructions = ["knn", "delaunay", "weibull_2"]
        mode_3D_instruction = [{"mode_3D": False}, {"mode_3D": True}]
        embedding_mode_instruction = [{"embedding_mode": "landmark_isomap", "embedded_dim": 32},
                              {"embedding_mode": "node2vec", "manifold_learning_mode": "UMAP", "embedded_dim": 32},
                              {"embedding_mode": "landmark_isomap", "embedded_dim": 128},
                              {"embedding_mode": "node2vec", "manifold_learning_mode": "UMAP", "embedded_dim": 128},
                              {"embedding_mode": "spring_relaxation"},
                              {"embedding_mode": "node2vec", "manifold_learning_mode": "PCA", "embedded_dim": 32},
                              {"embedding_mode": "shortest_paths", "manifold_learning_mode": "UMAP"},
                              {"embedding_mode": "shortest_paths", "manifold_learning_mode": "PCA"}]
        proximity_mode_instruction = [{"proximity_mode": prox_mode} for prox_mode in proximity_mode_list_instructions]
        instructions_iterator = itertools.product(mode_3D_instruction, embedding_mode_instruction, proximity_mode_instruction)


    Output
        CSV file for each set of parameters containing accuracy and computational complexity values
        Can be found in folder "/Appendix_Data/"

    """
    for instruction in instructions_iterator:
        print("INSTRUCTION", instruction)
        for parameter in instruction:  # parameter is a dictionary
            for k in list(parameter.keys()):  # Update parameters as instructed
                default_params[k] = parameter[k]
        if default_params["proximity_mode"] == "knn_weighted":
            default_params["weighting"] = "inverse_distance"

        default_params["align_to_original"] = False  # Do not compute distortion (some modes e.g. PCA
        # are not accurate enough)
        main_parameters = MainParameters(default_params)

        count = 0
        while True:
            try:
                tracemalloc.start()
                quality_metrics_dict = main_parameters.node_embedding_manifold_learning_main()
                plt.close('all')
                count += 1
                if count > 0:
                    break
            except Exception as e:
                logging.error('Error:' + str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error:", exc_type, fname, exc_tb.tb_lineno)
                pass
            else:
                break
        metrics_dict = {
            "KNN": quality_metrics_dict["KNN"],
            "CPD": quality_metrics_dict["CPD"],
            "Time": quality_metrics_dict["Time"],
            "Memory": quality_metrics_dict["Memory"]
        }
        tracemalloc.stop()
        quality_metrics_df = pd.DataFrame(metrics_dict, index=[0])
        df_path = os.getcwd() + "/Appendix_Data/"
        # Shorter names
        emb_mode = default_params["embedding_mode"]
        man_mode = default_params["manifold_learning_mode"]
        prox_mode = default_params["proximity_mode"]
        emb_dim = default_params["embedded_dim"]
        density = default_params["density"]
        dim = default_params["mode_3D"] + 2
        quality_metrics_df.to_csv(
            df_path + f"df_dec1222_{emb_mode}_{man_mode}_N={density}_dim={dim}_emb_dim={emb_dim}_{prox_mode}.csv",
            sep='\t')


def iterate_comp_complexity_data_utility(default_params, density_list):
    """
    Input
        default params: image recovery parameters

        density_list: set of density values, e.g. density_list = np.logspace(np.log10(8000), np.log10(100000), num=5)

    Output
        CSV file for each proximity mode containing accuracy / system size
        Can be found in folder "/Computational_Complexity_Plot/"
    """

    pre_df_mean_dic = {}
    pre_df_std_dic = {}
    for density in density_list:
        default_params["density"] = density
        pre_quality_df = []  # Append row values, afterwards transform into dataframe
        iterations = 1  # Set iterations to n to have n samples
        for _ in range(iterations):
            count = 0
            while True:
                try:
                    default_params["start_time"] = time.time()
                    tracemalloc.start()
                    main_parameters = MainParameters(default_params)
                    quality_metrics_dict = main_parameters.node_embedding_manifold_learning_main()

                    metrics_dict = {"KNN": quality_metrics_dict["KNN"],
                                    "CPD": quality_metrics_dict["CPD"],
                                    "Time": quality_metrics_dict["Time"],
                                    "Memory": quality_metrics_dict["Memory"]}
                    pre_quality_df.append(metrics_dict)
                    tracemalloc.stop()
                    print("METRICS: ", quality_metrics_dict)
                    if count > 10:  # If after 10 iterations a connected graph is not generated, break
                        break
                except:
                    pass
                else:
                    break

        comp_complex_metrics_dataframe = pd.DataFrame(pre_quality_df)
        # Get the mean and standard deviation
        mean_values = comp_complex_metrics_dataframe.mean()
        std_values = comp_complex_metrics_dataframe.std()
        # Get them on a list for further processing
        pre_df_mean_dic[density] = mean_values
        pre_df_std_dic[density] = std_values

    df_mean = pd.DataFrame(pre_df_mean_dic)
    df_std = pd.DataFrame(pre_df_std_dic)

    # Write dataframes
    embedding_mode = default_params["embedding_mode"]
    df_path = os.getcwd() + "/Computational_Complexity_Plot/"
    df_mean.to_csv(df_path + f"df_comp_complexity_{embedding_mode}", sep='\t')
    df_std.to_csv(df_path + f"df_std_{embedding_mode}", sep='\t')



class ValidatedSetterProperty:
    """
    Auxiliary class to ensure that some of the variables belong to a specified range of values:
    e.g. embedding mode can only be "node2vec", "landmark_isomap", "spring_relaxation"...
    """
    def __init__(self, func, name=None, doc=None):
        self.func = func
        self.__name__ = name if name is not None else func.__name__
        self.__doc__ = doc if doc is not None else func.__doc__
    def __set__(self, obj, value):
        ret = self.func(obj, value)
        obj.__dict__[self.__name__] = value

# Create argument dictionary from this
class Im_Rec_Arguments():
    """ Contains parameters to fine tune each reconstruction. The most relevant are the embedding mode, the
    manifold learning mode, the density (system size), the output dimension (mode_3D), plot_mode (to save figures),
    mode_anim (to save animations).

    Attributes
    ---------

    embedding_mode: str
        The kind of alogirthm to perform structural embedding: "node2vec", "ggvec",
        "landmark_isomap", "shortest_paths","spring_relaxation", "original_image"

    manifold_learning_mode: str
        The kind of algorithm to perform dimensionality reduction:"UMAP", "PCA", "directly", "original_image"

    density: int
        The system size, how many molecules (points) are to be reconstructed.

    mode_3D: bool
        True if the recovered image is 3-dimensional, False if it is 2-dimensional

    plot_mode: bool
        True if the user requires figures

    mode_anim: bool
        True if the user requires animated gifs (only available if mode_3D=True)

    start_time: float
        Time at which the computation starts

    title_edge_list: str
        Name of the document containing the list of edges with format "node1 node 2 weight"

    title_edge_list_experimental: str
        Name of the document containing the list of edges with format "node1 node 2 weight".
        User must manually specify the name of the document and make sure the document is found under
        /Input_Documents/Edge_Lists/

    exp_delimiter: str
        Delimiter for the edge list format. Default " ", comma separated value ","

    L: int
        Length of the hypercube
    partition: int
        Controls the amount of color partitions when coloring reconstructions

    mode_anim: bool
        If True, returns an animation in the "Reconstructed Animations" folder

    align_to_original: bool
        If True, computes distortion

    generate_new_knn_data: bool
        If True, a proximity graph is created

    generate_embedding_vectors: bool
        If True, perform structural embedding

    generate_dim_reduction: bool
        If True, perform dimensionality reduction / manifold learning

    weighting: str
        unweight", "distance", "inverse_distance", "softmax_inverse_distance

    pixel_art: str
        Type of coloring for the recovered image: 2D -->"swedish_flag", "pixel_monster", "mario", "mushroom",
        "star", "flower", "boo", "concentric_faces". 3D --> "tri_checkers", "mario_faces", "concentric_faces"

    walklen: int
        If node2vec, assign length of the random walks

    return weight: float
        If node2vec, assign return weight value (the higher the more BFS-like)

    neighbor weight: float
        If node2vec, assign neighbor weight value (the higher the more DFS-like)

    n_neighbors: int
        If UMAP, assign the average number of neighbors as a parameter

    n_neighbors_knn: int
        Determine how many neighbors when computing the local KNN quality metric

    proximity_mode: str
        Determine the kind of proximity graph: "knn", "epsilon-ball", "delaunay", "beta_multimodal",
        "weibull_decaying_1", "weibull_2", "weibull_3", "knn_weighted", "experimental"

    radius_range: float
        Assign a maximum value for epsilon for the e-ball proximity graph

    is_connected: bool
        Determine if the graph is connected (necessary to recover image)

    """
    def __init__(self, start_time=time.time(), title_edge_list="", title_edge_list_experimental="",
                 exp_delimiter = " ", L=1, partition=500, mode_3D=False,
                 mode_anim=False, align_to_original=False,
                 embedding_mode="node2vec", generate_new_knn_data=True, generate_embedding_vectors=True,
                 generate_dim_reduction=True, density=1000, embedded_dim=32, n_neighbors=15,
                 manifold_learning_mode="UMAP", weighting="unweight", knn_graph="knn",
                 pixel_art="concentric_faces", walklen=10, return_weight=1, neighbor_weight=1,
                 n_neighbors_knn=15, proximity_mode="knn", radius_range=0.5,
                 plot_mode=False, is_connected=True):

        self.start_time = start_time
        self.title_edge_list = title_edge_list
        self.title_edge_list_experimental = title_edge_list_experimental
        self.exp_delimiter = exp_delimiter
        self.L = L
        self.partition = partition
        self.mode_3D = mode_3D
        self.mode_anim = mode_anim
        self.generate_new_knn_data = generate_new_knn_data
        self.generate_embedding_vectors = generate_embedding_vectors
        self.generate_dim_reduction = generate_dim_reduction
        self.density = density
        self.embedded_dim = embedded_dim
        self.n_neighbors = n_neighbors
        self.knn_graph = knn_graph
        self.align_to_original = align_to_original
        self.walklen = walklen
        self.n_neighbors_knn = n_neighbors_knn
        self.radius_range = radius_range
        self.plot_mode = plot_mode
        self.is_connected = is_connected


        radius_coefficient = 3.5
        radius = (n_neighbors_knn / (radius_coefficient * density)) ** (1 / (mode_3D + 2))
        self.radius = radius
        self.proximity_mode = proximity_mode
        self.weighting = weighting
        self.pixel_art = pixel_art
        self.embedding_mode = embedding_mode
        self.manifold_learning_mode = manifold_learning_mode

        if self.embedding_mode != "node2vec":
            self.walklen, self.return_weight, self.neighbor_weight, self.node2vec_parameters = None, None, None, ""
        else:
            self.walklen = 10  # Default: 10
            self.return_weight = 1  # Default: 1       Setting this high: BFS
            self.neighbor_weight = 1  # Default: 1     Setting this high: DFS
            q = 1 / self.return_weight  # inverse of return_weight is q, as described in node2vec paper
            p = 1 / self.neighbor_weight  # inverse of neighbor_weight is p, as described in node2vec paper
            self.node2vec_parameters = tuple([q, p, self.walklen])



    @ValidatedSetterProperty
    def proximity_mode(self, value):
        if value not in ("knn", "epsilon-ball", "delaunay", "beta_multimodal", "weibull_decaying_1", "weibull_2",
                       "weibull_3", "knn_weighted", "experimental"):
            raise ValueError("Please input a valid proximity mode. Possible modes: "
                             "knn", "epsilon-ball", "delaunay", "beta_multimodal", "weibull_decaying_1", "weibull_2",
                             "weibull_3", "knn_weighted", "experimental")
    @ValidatedSetterProperty
    def weighting(self, value):
        if value not in ("unweight", "distance", "inverse_distance", "softmax_inverse_distance"):
            raise ValueError("Please input a valid weighting mode. Possible modes: "
                             "unweight", "distance", "inverse_distance", "softmax_inverse_distance")
    @ValidatedSetterProperty
    def pixel_art(self, value):
        if value not in ("swedish_flag", "pixel_monster", "mario", "mushroom", "star", "flower",
                             "boo", "tri_checkers", "mario_faces", "concentric_faces"):
            raise ValueError("Please input a valid pixel art mode. Possible modes: "
                             "swedish_flag", "pixel_monster", "mario", "mushroom", "star", "flower",
                             "boo", "tri_checkers", "mario_faces", "concentric_faces")

    @ValidatedSetterProperty
    def embedding_mode(self, value):
        if value not in ("node2vec", "ggvec", "landmark_isomap", "shortest_paths",
                                  "spring_relaxation", "original_image"):
            raise ValueError("Please input a valid structural embedding mode. Possible modes: "
                             "node2vec", "ggvec", "landmark_isomap", "shortest_paths",
                             "spring_relaxation", "original_image")
        if value == "node2vec":
            self.walklen = 10  # Default: 10
            self.return_weight = 1  # Default: 1       Setting this high: BFS
            self.neighbor_weight = 1  # Default: 1     Setting this high: DFS
            q = 1 / self.return_weight  # inverse of return_weight is q, as described in node2vec paper
            p = 1 / self.neighbor_weight  # inverse of neighbor_weight is p, as described in node2vec paper
            self.node2vec_parameters = tuple([q, p, self.walklen])

    @ValidatedSetterProperty
    def manifold_learning_mode(self, value):
        if value not in ("UMAP", "PCA", "directly", "original_image"):
            raise ValueError("Please input a valid manifold learning mode. Possible modes: "
                             "UMAP", "PCA", "directly", "original_image")



def recover_image(default_params):
    """
    INPUT:
        default_params: Parameters for image recovery defined in class Im_Rec_Arguments

    OUTPUT:
        quality_metrics_dict: dictionary containing accuracy / empirical computational complexity of the reconstruction

        *CSV files under /Input_Documents/ containing:
            -Edge list
            -Label list (coloring of the recover image)
            -Positions and neighbors (original positions, neighbors for each molecule,
                                      distance from neighbors, neighbor weight)

        *CSV files under /Output_Documents containing:
            -Embedded positions: recovered positions to be compared with original positions
            -Embedded vectors: 1xD vectors created during structural embedding (D=32 by default)
            -Distortion plot: if plot_mode=True and align_to_original=True, distortion plots are found in this folder

        if default_params["plot_mode"]=True:
        *Figure files under /Reconstructed_Figures/: colored (labeled) recovered images
        *Gif files under /Reconstructed_Animations/: animations for (only) 3D recovered images

    """

    # Point cloud alignment (for distortion plots) does not always converge, try several seeds if cloud alignment
    if default_params["align_to_original"] and default_params["plot_mode"]:
        quality_metrics_dict = recover_image_try_different_seeds(default_params)
    else:
        tracemalloc.start()
        main_parameters = MainParameters(default_params)  # Establish parameters
        quality_metrics_dict = main_parameters.node_embedding_manifold_learning_main()  # Call main function
    return quality_metrics_dict


