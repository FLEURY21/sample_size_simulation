#############################################################################################
#| Program name: run_simulation_terminal_job.py                                             #
#| Description: Process simulations and graphics sample size. Code must be use in terminal  #
#|              command line process                                                        #
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
import argparse
from tabulate import tabulate

# Program
#---------
# Parameters process
parser = argparse.ArgumentParser(
        prog = 'run_simulation_terminal_job',
        description = "This program process at sample size calculation\tby Monte Carlo simulation.")
parser.add_argument('-start', type = int, help = 'Maximal cohort size.')
parser.add_argument('-end', type = int, help = 'Minimal cohort size.')
parser.add_argument('-NumSimu', type = int, help = 'Number of simulation.')
parser.add_argument('-epsilonH0', type = float, help = 'Value expected under H0 hypothesis.')
parser.add_argument('-epsilonH1', type = float, help = 'Value expected under H1 hypothesis.')
parser.add_argument('-H0', type = float, help = 'H0 hypothesis in bilateral mode.')
parser.add_argument('-alpha', type = float, help = 'Alpha value.')
parser.add_argument('-power', type = float, help = 'Power value.')
parser.add_argument('-method', type = str, choices=['arcsinus', 'beta', 'wilson', 'normal'], help = 'Binomial confidence interval method.')
parser.add_argument('-OutputPath', type = str, default='None', help = 'Output path where figures will be generated. If None (in string format) value then OUTPUTS file will be automaticaly generated.')
args = parser.parse_args()
# Simulation
data = api(args.start, args.end, args.NumSimu, args.epsilonH0, args.epsilonH1, args.H0, args.alpha, args.power, args.method)
# Graphical results
graph_api(args.start, args.end, args.NumSimu, args.epsilonH0, args.epsilonH1, args.H0, args.alpha, args.power, args.method, output_path=args.OutputPath)
if args.OutputPath == "None":
    print("\n\n\n\t\t\tGraphics are generated in OUTPUTS directory.")
else:
    print("\n\n\n\t\t\tGraphics are generated in " + str(args.OutputPath) + " directory.")
print("\n\nOptimal sample size found are :")
print("================================\n")
print(tabulate(data, headers='keys', tablefmt='psql', showindex=False))
