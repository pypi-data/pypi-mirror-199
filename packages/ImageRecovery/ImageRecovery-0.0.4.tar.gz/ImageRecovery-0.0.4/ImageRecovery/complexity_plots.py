import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


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

def get_df(plot_dir, df_names):

    os.chdir(plot_dir)

    df_dict = {}
    for name in df_names:
        df_dict[name] = pd.read_csv(name, sep="\t")  # mean
    return df_dict

def preprocess_df_comp_complex_plot(df_mean, delete_first_outlier):
    """
    Preprocess dataframes so they can be managed properly
        df_mean : metrics data (averaged if more than one iteration)
        delete_first_outlier: if True, deletes the first point (sometimes outlier due to computer precompiling)
    """
    data_dict = {"N_list": np.delete(np.array(df_mean.columns),0),
    "time_list": np.delete(np.array(df_mean.transpose()[2]),0),
    "memory_list": np.delete(np.array(df_mean.transpose()[3]),0)}

    if delete_first_outlier:
        data_dict = {k: data_dict[k][1:] for k in data_dict}
    return data_dict



def plot_comp_complex(data_dict, plot_dir):
    fig,ax = plt.subplots()
    # Plot 1st axis

    for i, element in enumerate(data_dict["N_list"]):
        N = float(element)   # Transform string to float and round it up to 2 decimals
        data_dict["N_list"][i] = N

    ax.errorbar(data_dict["N_list"], data_dict["time_list"],  color='blue', marker='o',
            linewidth=3, label="Time")
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.plot()
    ax.set_xlabel('# Nodes')
    ax.set_ylabel('Time (s)', color="blue")


    ax2 = ax.twinx()

    # Plot 2nd axis
    ax2.errorbar(data_dict["N_list"], data_dict["memory_list"], color='orange', marker ='o',
             linewidth=3, label="Memory Peak")
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_ylabel('Peak memory (MB)', color="orange")

    # Align to 0
    # ax.set_ylim(bottom=0)
    # ax2.set_ylim(bottom=0)

    # add second y-axis label
    plt.savefig(f"{plot_dir}comp_complex_plot.pdf")

def plot_comp_complex_v2(data_dict1, data_dict2, plot_dir):
    plt.style.use("science")
    plt.rcParams['font.size'] = '18'
    fig,ax = plt.subplots()


    # Plot 1st axis
    length = len(data_dict1["N_list"])
    # Transform string to float for the x axis
    for i, element in enumerate(data_dict1["N_list"]):
        N = float(element)   # Transform string to float and round it up to 2 decimals

        data_dict1["N_list"][i] = N
    for i, element in enumerate(data_dict2["N_list"]):
        N = float(element)
        data_dict2["N_list"][i] = N





    # Skip first element (outlier because of preprocess/inicialization)
    # data_dict1["N_list"] = data_dict1["N_list"][1:]
    # data_dict2["N_list"] = data_dict2["N_list"][1:]

    # Log transform
    data_dict1["N_list"] = np.log10(data_dict1["N_list"].astype(float))
    data_dict2["N_list"] = np.log10(data_dict2["N_list"].astype(float))
    data_dict1["time_list"] = np.log10(data_dict1["time_list"].astype(float))
    data_dict2["time_list"] = np.log10(data_dict2["time_list"].astype(float))


    theta_1, MSE1, R2_1 = linear_regression_from_np_arrays(data_dict1["N_list"], data_dict1["time_list"])
    theta_2, MSE2, R2_2 = linear_regression_from_np_arrays(data_dict2["N_list"], data_dict2["time_list"])


    # Reverse log transform
    data_dict1["N_list"] = np.power(10, data_dict1["N_list"].astype(float))
    data_dict2["N_list"] = np.power(10, data_dict2["N_list"].astype(float))
    data_dict1["time_list"] = np.power(10, data_dict1["time_list"].astype(float))
    data_dict2["time_list"] = np.power(10, data_dict2["time_list"].astype(float))

    ax.plot(data_dict1["N_list"], data_dict1["time_list"], c="#009ADE", marker='o',
            linewidth=0)
    ax.plot(data_dict2["N_list"], data_dict2["time_list"], c="#FF1F5B", marker='o',
            linewidth=0)

    # ax.set_yscale('function', functions=(partial(np.power, 10.0), np.log10))   # maybe for future tweaking the axis scale

    # Plot regression lines
    a1 = theta_1[0]
    a2 = theta_2[0]
    b1 = 10**(theta_1[1]/theta_1[0])    # Conversion from log to regular scale
    b2 = 10**(theta_2[1]/theta_2[0])

    line1 = (b1 * data_dict1["N_list"])**theta_1[0]
    line2 = (b2 * data_dict2["N_list"])**theta_2[0]

    # line1 = theta_1[0] * data_dict1["N_list"] + theta_1[1]
    # line2 = theta_2[0] * data_dict2["N_list"] + theta_2[1]

    str_b1 = str(b1[0])[:5]
    str_b2 = str(b2[0])[:5]
    str_a1 = str(a1[0])[:4]
    str_a2 = str(a2[0])[:4]
    ax.plot(data_dict1["N_list"], line1, c="#009ADE", label=r'Staged: $y='+str_b1+r'x^{'+str_a1+r'}$')
    ax.plot(data_dict2["N_list"], line2, c="#FF1F5B",  label=r'Not staged: $y='+str_b2+r'x^{'+str_a2+r'}$')
    ax.legend(frameon=False,   bbox_to_anchor=(0.4, 1.5), loc='upper center')
    ax.set_yscale('log')
    ax.set_xscale('log')

    # Remove scientific notation from the log-log axis
    # ax.xaxis.get_major_formatter().set_scientific(False)
    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

    # # Remove top and right axis
    # ax.spines.right.set_visible(False)
    # ax.spines.top.set_visible(False)
    # ax.yaxis.set_ticks_position('left')
    # ax.xaxis.set_ticks_position('bottom')

    ax.set_xlabel('N')
    ax.set_ylabel('Time (s)')
    ax.plot()

    plt.savefig(f"{plot_dir}comp_complex_plot.pdf")
    plt.show()
    plt.close()


    # # Complexity plot with long  times!
    # fig2, ax2 = plt.subplots()
    # N_list = [50000, 100000, 200000, 300000]
    # time_list = [413.26278924942,  555.381717205048,  730.763995170593, 990.36192353249]
    # ax2.set_xlabel('Nodes')
    # ax2.set_ylabel('Time (s)')
    # ax2.set_xlim([0, max(N_list)+10000])
    # ax2.plot(N_list, time_list, color='green', marker='o', linewidth=0, label="GBIR")
    #
    # # # Delete boarders
    # # ax2.spines.right.set_visible(False)
    # # ax2.spines.top.set_visible(False)
    # # ax2.yaxis.set_ticks_position('left')
    # # ax2.xaxis.set_ticks_position('bottom')
    #
    #
    # ax2.legend(fontsize=13, frameon=False)
    # plt.savefig(f"{plot_dir}comp_complex_plot.pdf")

def plot_comp_complex_v2_memory(data_dict1, data_dict2, plot_dir):
    plt.rcParams['font.size'] = '18'
    plt.style.use("science")
    fig,ax = plt.subplots()


    # Plot 1st axis
    length = len(data_dict1["N_list"])
    # Transform string to float for the x axis
    for i, element in enumerate(data_dict1["N_list"]):
        N = float(element)   # Transform string to float and round it up to 2 decimals

        data_dict1["N_list"][i] = N
    for i, element in enumerate(data_dict2["N_list"]):
        N = float(element)
        data_dict2["N_list"][i] = N





    # Skip first element (outlier because of preprocess/inicialization)
    # data_dict1["N_list"] = data_dict1["N_list"][1:]
    # data_dict2["N_list"] = data_dict2["N_list"][1:]

    # Scale transform (MB to GB)
    data_dict1["memory_list"] = data_dict1["memory_list"].astype(float) /1024
    data_dict2["memory_list"] = data_dict2["memory_list"].astype(float) /1024

    # Log transform
    data_dict1["N_list"] = np.log10(data_dict1["N_list"].astype(float))
    data_dict2["N_list"] = np.log10(data_dict2["N_list"].astype(float))
    data_dict1["memory_list"] = np.log10(data_dict1["memory_list"].astype(float))
    data_dict2["memory_list"] = np.log10(data_dict2["memory_list"].astype(float))


    theta_1, MSE1, R2_1 = linear_regression_from_np_arrays(data_dict1["N_list"], data_dict1["memory_list"])
    theta_2, MSE2, R2_2 = linear_regression_from_np_arrays(data_dict2["N_list"], data_dict2["memory_list"])


    # Reverse log transform
    data_dict1["N_list"] = np.power(10, data_dict1["N_list"].astype(float))
    data_dict2["N_list"] = np.power(10, data_dict2["N_list"].astype(float))
    data_dict1["memory_list"] = np.power(10, data_dict1["memory_list"].astype(float))
    data_dict2["memory_list"] = np.power(10, data_dict2["memory_list"].astype(float))

    ax.plot(data_dict1["N_list"], data_dict1["memory_list"], c="#009ADE", marker='o',
            linewidth=0)
    ax.plot(data_dict2["N_list"], data_dict2["memory_list"], c="#FF1F5B", marker='o',
            linewidth=0)

    # ax.set_yscale('function', functions=(partial(np.power, 10.0), np.log10))   # maybe for future tweaking the axis scale

    # Plot regression lines
    a1 = theta_1[0]
    a2 = theta_2[0]
    b1 = 10**(theta_1[1]/theta_1[0])    # Conversion from log to regular scale
    b2 = 10**(theta_2[1]/theta_2[0])

    line1 = (b1 * data_dict1["N_list"])**theta_1[0]
    line2 = (b2 * data_dict2["N_list"])**theta_2[0]

    # line1 = theta_1[0] * data_dict1["N_list"] + theta_1[1]
    # line2 = theta_2[0] * data_dict2["N_list"] + theta_2[1]

    str_b1 = str(b1[0])[:6]
    str_b2 = str(b2[0])[:6]
    str_a1 = str(a1[0])[:4]
    str_a2 = str(a2[0])[:4]
    ax.plot(data_dict1["N_list"], line1, c="#009ADE", label=r'Staged: $y='+str_b1+r'x^{'+str_a1+r'}$')
    ax.plot(data_dict2["N_list"], line2, c="#FF1F5B",  label=r'Not staged: $y='+str_b2+r'x^{'+str_a2+r'}$')
    ax.legend(frameon=False,   bbox_to_anchor=(0.4, 1.5), loc='upper center')
    ax.set_yscale('log')
    ax.set_xscale('log')

    # Remove scientific notation from the log-log axis
    # ax.xaxis.get_major_formatter().set_scientific(False)
    ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter())

    # # Remove top and right axis
    # ax.spines.right.set_visible(False)
    # ax.spines.top.set_visible(False)
    # ax.yaxis.set_ticks_position('left')
    # ax.xaxis.set_ticks_position('bottom')

    ax.set_xlabel('N')
    ax.set_ylabel('Memory (GB)')
    ax.plot()

    plt.savefig(f"{plot_dir}comp_complex_plot_memory.pdf")
    plt.show()
    plt.close()

def get_parent_dir():
    parent_dir = os.getcwd()
    return parent_dir

def get_comp_complexity_both_plots():
    """
    Main function to get both -time and space- computational complexity,
    for both -node2vec and only umap- reconstructions
    """
    parent_dir = get_parent_dir()
    plot_dir = f"{parent_dir}/Computational_Complexity_Plot/"

    # Data documents
    df_names1 = ["df_comp_complexity_node2vec_8000_1000000"]
    df_names2 = ["df_comp_complexity_shortest_paths_8000_45000"]
    # Create dictionaries
    df_dict1 = get_df(plot_dir, df_names1)
    df_dict2 = get_df(plot_dir, df_names2)

    delete_first_if_outlier = False  # Depending on computer (package precomp) first element can be outlier
    # Preprocess dictionaries
    data_dict1 = preprocess_df_comp_complex_plot(df_dict1[df_names1[0]],  delete_first_if_outlier)
    data_dict2 = preprocess_df_comp_complex_plot(df_dict2[df_names2[0]],  delete_first_if_outlier)
    # Plot
    plot_comp_complex_v2(data_dict1, data_dict2, plot_dir)
    plot_comp_complex_v2_memory(data_dict1, data_dict2, plot_dir)

# # RUN - Uncomment below
# get_comp_complexity_both_plots()



