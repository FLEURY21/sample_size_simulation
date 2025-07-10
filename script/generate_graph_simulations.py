__docformat__ = "google"
#############################################################################################
#| Program name: genearate_graph_simulations.py                                             #
#| Description: Generate simulation graph results to verify alpha and beta error and        #
#|              evaluate the best IC method to choose for your sample size process          #
#|                                                                                          #
#| Author: Maxime FLEURY - Institut Paoli Calmettes - Biostatistics and methodology Unit    #
#| Current programmer: Maxime Fleury                                                        #
#| Origine date: 3 July 2025                                                                #
#| Last modification: 3 July 2025                                                           #
#| Version: 1.0                                                                             #
#| Input (programs and data): simulations.py                                                #
#| Output (programs and data):                                                              #
#############################################################################################

# Imports
#---------
# Import simulations function
from .simulations import *
# Python imports
import os
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

# functions
#-----------

def create_output_file():
    """@private
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.join(current_dir, '..')
    folder_path = os.path.join(parent_dir, 'OUTPUTS')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def parameter_analysis_1(data_simulation, alpha, output_path="None"):
    """
    Generate alpha evolution with Monte Carlo parameters of the 
    sample size process, returns a matplotlib Figure.

    Args:
        data_simulation (pandas dataframe): sample size process data
        alpha (float): Target alpha level
        output_path (str, optional): Output figures path. Defaults to "None".
                                    If default value then OUTPUT file is created
                                    and figures are saved in this file.

    Returns:
        fig (matplotlib.figure.Figure): The matplotlib figure
    """
    title_fig1 = "alpha_evolution_method"
    methods = sorted(set(data_simulation["method"]))
    l = []
    fig = plt.figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    for method in methods:
        data = data_simulation[data_simulation["method"] == method]
        ax.plot(data["size"], data["alpha"], label=method)
        l.append(method)
    if not data.empty:
        y = [alpha] * len(data["size"])
        ax.plot(data["size"], y, color="red", linestyle="--", label="Target alpha")
    ax.set_xlabel("Sample size")
    ax.set_ylabel("Alpha")
    ax.set_title("Alpha evolution")
    ax.legend()
    if output_path != "no save":
        if output_path == "None":
            folder_path = create_output_file()
            output_path1 = os.path.join(folder_path, title_fig1)
        else:
            output_path1 = os.path.join(output_path, title_fig1)
        fig.savefig(output_path1 + ".png", format="png", bbox_inches='tight')
    return fig

def mse_graphics_analysis_2(simulation_data, output_path="None"):
    """Generate Matplotlib figure which study evolution of MSE scores
    between simulated alpha and alpha computed by formula and same 
    reasonment with power.

    Args:
        simulation_data (pandas dataframe): simulation data
        output_path (str, optional): Output figures path. Defaults to "None".
                                    If default value then OUTPUT file is created
                                    and figures are saved in this file.

    Returns:
        matplotlib figure: The matplotlib figure.
    """
    title_fig1 = "MSE_evolution_" +  list(set(simulation_data["method"]))[0]
    if output_path == "None":
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.join(current_dir, '..')
        folder_path = os.path.join(parent_dir, 'OUTPUTS')
        output_path1 = os.path.join(folder_path, title_fig1)
    else:
        output_path1 = output_path + title_fig1
    fig = plt.figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(simulation_data["size"], simulation_data["mse_alpha"])
    ax.plot(simulation_data["size"], simulation_data["mse_power"])
    ax.set_xlabel("Sample size")
    ax.set_ylabel("MSE score")
    ax.set_title("Evolution of MSE score")
    ax.legend(["Alpha", "Power"])
    if output_path != "no save":
        fig.savefig(output_path1 + ".png", format="png", bbox_inches='tight')
    return fig


def parameter_analysis_2(data_simulation, power, output_path="None"):
    """
    Generate power evolution with Monte Carlo parameters of the 
    sample size process.

    Args:
        data_simulation (pandas dataframe): sample size process data
        power (float): Target power level
        output_path (str, optional): Output figures path. Defaults to "None".
                                    If default value then OUTPUT file is created
                                    and figures are saved in this file.

    Returns:
        matplotlib figure: The matplotlib figure.
    """
    title_fig = "power_evolution_method"
    methods = sorted(set(data_simulation["method"]))
    fig = plt.figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    for method in methods:
        data = data_simulation[data_simulation["method"] == method]
        ax.plot(data["size"], data["power"], label=method)
    if not data.empty:
        y = [power] * len(data["size"])
        ax.plot(data["size"], y, color="red", linestyle="--", label="Target power")
    ax.set_xlabel("Sample size")
    ax.set_ylabel("Power")
    ax.set_title("Power evolution")
    ax.legend()
    if output_path != "no save":
        if output_path == "None":
            folder_path = create_output_file()
            output_path_full = os.path.join(folder_path, title_fig)
        else:
            output_path_full = os.path.join(output_path, title_fig)
        fig.savefig(output_path_full + ".png", format="png", bbox_inches='tight')
    return fig

def graph_api(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat, output_path="None"):
    """Function which process and generate sample size graphical analysis with one statistical method choice. It this function
    which must call to generate all graphics.

    Args:
        cohort_size_start (int): Maximal cohort size
        cohort_size_end (int): Minimal cohor size
        num_simu (int): Number of simulation for each run
        epsilon_H0 (float): proportion expected under H0 (bibliography result). Control alpha error.
        epsilon_H1 (float): Proportion value under H1. Control beta error.
        H0 (float): H0 hypothesis in bilateral conformation.
        alpha (float): alpha value
        power (float): beta value
        method_stat (string): IC method name to estimate Binomial IC (cf compute_IC_binomial function).
        output_path (str, optional): Output figures path. Defaults to "None".
                                    If default value then OUTPUT file is created
                                    and figures are saved in this file.

    Returns:
        tuple: Return a tuple of figures.
    """
    data_simu = monte_carlo_process_binomial(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat)
    create_output_file()
    fig1 = parameter_analysis_1(data_simu, alpha, output_path=output_path)
    fig2 = parameter_analysis_2(data_simu, power, output_path=output_path)
    fig3 = mse_graphics_analysis_2(data_simu, output_path=output_path)
    return fig1, fig2, fig3

def multi_process_graph_api(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, list_method_stat, output_path="None"):
    """Function which process and generate sample size graphical analysis for many statistical method (see monte_carlo_process_binomial documentation). It this function
    which must call to generate all graphics.

    Args:
        cohort_size_start (int): Maximal cohort size
        cohort_size_end (int): Minimal cohor size
        num_simu (int): Number of simulation for each run
        epsilon_H0 (float): proportion expected under H0 (bibliography result). Control alpha error.
        epsilon_H1 (float): Proportion value under H1. Control beta error.
        H0 (float): H0 hypothesis in bilateral conformation.
        alpha (float): alpha value
        power (float): beta value
        list_method_stat (list): list of statistical method to compute confidence interval of a binomial distribution (normal, wilson, arcsinus, beta)
        output_path (str, optional): Output figures path. Defaults to "None".
                                    If default value then OUTPUT file is created
                                    and figures are saved in this file.
    """
    simu_obj_list = []
    for method in list_method_stat:
        data_simu = monte_carlo_process_binomial(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method)
        simu_obj_list.append(data_simu)
    data_simulation = pd.concat(simu_obj_list, axis=0,ignore_index=True)
    parameter_analysis_1(data_simulation, alpha, output_path=output_path)
    parameter_analysis_2(data_simulation, power, output_path=output_path)
