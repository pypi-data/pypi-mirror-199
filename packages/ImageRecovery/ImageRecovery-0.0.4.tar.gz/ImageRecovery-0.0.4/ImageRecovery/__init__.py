import os

from image_recovery_main import *
from scalability_vs_metrics_plot import run_scalability_vs_metrics_plot_2d_and_3d
from complexity_plots import get_comp_complexity_both_plots
from plot_distortion_from_file import plot_all_dist_lines_fig3

# Scripts that contain executables


### START


# Create folders:
code_dir = os.getcwd()  # Code directory
os.chdir("..")  # Parent directory where data folders are
parent_dir = os.getcwd()
create_folder_structure(parent_dir)


# Timers:
first_initial_time = time.time()  # Set timer for all process
start_time = time.time()  # Set timer for each iteration (will change on iteration)





