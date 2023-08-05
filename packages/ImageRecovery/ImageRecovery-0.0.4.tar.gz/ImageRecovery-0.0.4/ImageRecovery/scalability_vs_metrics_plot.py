import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt



def plot_metric(metric_name, files, color_proxmode_dic, plot_dir, mode_3D, proximity_mode_list):
    metric_prox_list = []    #contains the value of the metric for each proximity graph
    prox_mode_list = []

    for file in files:   # for every proximity mode
        # print(file, metric_name)

        df = pd.read_csv(file, sep="\t")
        proximity_mode = file[3:-4]
        metric = df[metric_name]
        metric_prox_list.append(metric)

        prox_mode_list.append(proximity_mode)
        N_list = df["N"]



    plt.style.use("science")
    plt.rcParams['font.size'] = '18'

    fig = plt.figure()
    # Iterate over the 8 proximity graphs for a specific quality metric

    for (i,metric_list) in enumerate(metric_prox_list):

        # Create zoom-out plot
        ax = plt.scatter(N_list, metric_list, color=color_proxmode_dic[proximity_mode_list[i]], alpha=1,  s=2, linewidths=1)
        plt.plot(N_list, metric_list, color=color_proxmode_dic[proximity_mode_list[i]], alpha=0.3,
                 label=proximity_mode_list[i])
        # y axis limit for 1) KNN, 2) CPD, 3) Distortion
    if metric_name == "KNN":
        plt.ylim(0, 1)
    elif metric_name == "CPD":
        plt.ylim(0, 1)
    elif metric_name == "Distortion":
        plt.ylim(0, 0.15)
    plt.xlabel("N")
    plt.ylabel(f"{metric_name}")

    # Zoom in ax

    plt.rcParams['font.size'] = '8'


    ## FOR 2D DATA
    ## [left, bottom, width, height]
    # if metric_name == "KNN":
    #     plt.rcParams['font.size'] = '6'
    #     ax_new = fig.add_axes(
    #         [0.205, 0.175, 0.3, 0.3])  # the position of zoom-out plot compare to the ratio of zoom-in plot
    # elif metric_name == "CPD":
    #     ax_new = fig.add_axes(
    #         [0.37, 0.35, 0.3, 0.3])  # the position of zoom-out plot compare to the ratio of zoom-in plot
    # else:
    #     ax_new = fig.add_axes(
    #         [0.37, 0.45, 0.3, 0.3])  # the position of zoom-out plot compare to the ratio of zoom-in plot

    ## FOR 3D DATA
    # [left, bottom, width, height]
    if metric_name == "Distortion":
        ax_new = fig.add_axes(
            [0.37, 0.45, 0.3, 0.3])  # the position of zoom-out plot compare to the ratio of zoom-in plot
    elif metric_name == "CPD":
        ax_new = fig.add_axes(
            [0.37, 0.35, 0.3, 0.3])  # the position of zoom-out plot compare to the ratio of zoom-in plot
    else:
        ax_new = fig.add_axes(
            [0.37, 0.2, 0.3, 0.3])  # the position of zoom-out plot compare to the ratio of zoom-in plot
    for (i,metric_list) in enumerate(metric_prox_list):

        ## Create zoom-in plot

        ax_new.scatter(N_list, metric_list, color=color_proxmode_dic[proximity_mode_list[i]], alpha=0.7,  s=0.5, linewidths=0.5)
        ax_new.plot(N_list, metric_list, color=color_proxmode_dic[proximity_mode_list[i]], alpha=0.5, label=proximity_mode_list[i])




    global_max = 0.001
    global_min = 1000
    for metric_list in metric_prox_list:
        max_value = max(metric_list)
        min_value = min(metric_list)
        if max_value > global_max:
            global_max = max_value
        if min_value < global_min:
            global_min = min_value
    plt.ylim(global_min-global_max/100, global_max+global_max/100)

    plt.rcParams['font.size'] = '18'



    # Write variations (for robustness analysis)
    difference_for_same_N = []
    for j in range(len(metric_prox_list[0])):  # N list
        prox_graph_value_for_same_N = []
        for i in range(len(metric_prox_list)):  # proximity graphs
            prox_graph_value_for_same_N.append(metric_prox_list[i][j])

        max_prox_graph = max(prox_graph_value_for_same_N)
        min_prox_graph = min(prox_graph_value_for_same_N)
        difference_max_min = max_prox_graph - min_prox_graph
        difference_for_same_N.append(difference_max_min)
    textfile = open(f"difference_magnitude_{metric_name}_dim={mode_3D+2}.txt", "w")
    for element in difference_for_same_N:
        textfile.write(str(element) + "\n")


    difference_for_same_N = np.array(difference_for_same_N)
    mean_difference = np.mean(difference_for_same_N)
    max_difference = np.max(difference_for_same_N)
    textfile.write("mean variation:" +  str(mean_difference) + "\n")
    textfile.write("max variation:" +  str(max_difference) + "\n")
    textfile.close()
    plt.savefig(f"{plot_dir}{metric_name}_N={max(N_list)}_dim={mode_3D+2}.pdf")
    plt.show()



def get_parent_dir():
    parent_dir = os.getcwd()
    return parent_dir
def plot_KNN_CPD_Distortion(mode_3D):
    """
    Get quality metrics plots (KNN, CPD and Distortion) for each proximity graph
    Input: mode_3D :: Bool  True if data comes from 3D space, False if it comes from 2D
    """
    parent_dir = get_parent_dir()
    plot_dir = f"{parent_dir}/Scalability_vs_Metrics_Plot/"
    proximity_mode_list = ["knn", "epsilon-ball", "delaunay", "weibull_decaying_1",
                           "beta_multimodal", "weibull_2", "weibull_3", "weighted_knn"]
    colors = ["#FF1F5B", "#00CD6C", "#F28522", "#A6761D", "#009ADE", "#AF58BA", "#FFC61E", "#ff9287"]
    color_proxmode_dic = dict(zip(proximity_mode_list, colors))

    files = [file for file in os.listdir(plot_dir) if file[-5:] == f"{mode_3D+2}.csv"]

    metrics = ["KNN", "CPD", "Distortion"]
    os.chdir(plot_dir)

    for metric_name in metrics:
        plot_metric(metric_name, files, color_proxmode_dic, plot_dir, mode_3D, proximity_mode_list)
    os.chdir("..")

def run_scalability_vs_metrics_plot_2d_and_3d():
    """
    Creates figures to analyze accuracy dependence with system size
    It also generates documents to compare accuracy difference between proximity graphs:
        e.g. "difference_magnitude_KNN.txt"
    """
    mode_3D_list = [False, True]
    for mode_3D in mode_3D_list: # Plot 2D and 3D
        plot_KNN_CPD_Distortion(mode_3D)
# # Uncomment to run
#run_scalability_vs_metrics_plot_2d_and_3d()