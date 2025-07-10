#############################################################################################
#| Program name: run_simulation_MAIN.py                                                     #
#| Description: Process simulations and graphics sample size. Parameters and code must be   #
#|              modificate in this program. This progrom is not to be run in command line   #
#|             terminal process                                                             #
#|                                                                                          #
#| Author: Maxime FLEURY - Institut Paoli Calmettes - Biostatistics and methodology Unit    #
#| Current programmer: Maxime Fleury                                                        #
#| Origine date: 3 July 2025                                                                #
#| Last modification: 3 July 2025                                                           #
#| Version: 2.0                                                                             #
#| Input (programs and data): simulations.py, generate_graph_simulations.py                 #
#| Output (programs and data): - If None parameter used the OUTPUT file is created          #
#|                               - alpha_evolution_method.png                               #
#|                               - power_evolution_method.png                               #
#|                               - MSE_evolution_method.png                                 #
#############################################################################################

# Import
#--------
from script.simulations import *
from script.generate_graph_simulations import *


# Parameters
#------------

# Statistics Test parameters
alpha = 0.05
power = 0.8
epsilon_H0 = 0.7
epsilon_H1 = 0.8
H0 = 0.7
method_stat = "wilson"
# Simulation parameter
cohort_size_start = 200
cohort_size_end = 10
num_simu = 1000

# Program
#---------
# Simulation
data = api(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat)
# Graphical results
graph_api(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat, output_path="None")

# The follow line code is an example of a simulation with many method to compare graphicly IC method estimation. Please don't pass the following line in comment and pass
# pass graph_api function in comment if you want use multi_process_graph_api function.

#multi_process_graph_api(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, ["wilson", "arcsinus", "normal", "beta"], output_path="None")