__docformat__ = "google"
#############################################################################################
#| Program name: simulation.py                                                              #
#| Description: Generate Monte Carlo simulations under H0 and H1 hypothesis for             #
#|              a sample size processing                                                    #
#|                                                                                          #
#| Author: Maxime FLEURY - Institut Paoli Calmettes - Biostatistics and methodology Unit    #
#| Current programmer: Maxime Fleury                                                        #
#| Origine date: 3 July 2025                                                                #
#| Last modification: 3 July 2025                                                           #
#| Version: 1.0                                                                             #
#| Input (programs and data): None                                                          #
#| Output (programs and data): None                                                         #
#############################################################################################

# Imports
#---------
import math
import numpy as np
import pandas as pd
from scipy.stats import norm
import scipy.stats as stats
from statsmodels.stats.proportion import proportion_confint
import time

###############################################################################

# Functions
#-----------

def generate_cohorte_binom(n, p, size):
    """Generate a binomial cohort of patients.
       Succes = 1
       echec = 0
    Args:
        n (int): bernouilli parameter (1 classical bernouilli)
        p (float): probability of succes
        size (_type_): cohort size

    Returns:
        numpy array: cohort size with succes and echec statut for each patient.
    """
    cohort =  np.random.binomial(n, p, size)
    return cohort

def compute_IC_binomial(cohort, alpha, method_stat):
    """Compute confidence interval (IC) for a Binomial distribution.

    Args:
        cohort (int): cohort size.
        alpha (float): alpha value ( must be between 0 and 1).
        method_stat (string): method to esticmate Binomila IC (beta, arcsinus, normal, wilson).
                              See https://www.statsmodels.org/dev/generated/statsmodels.stats.proportion.proportion_confint.html.

    Returns:
        tuple: IC lower, IC upper
    """
    cohort_1 = cohort[cohort == 1]
    if method_stat == "arcsinus":
        p_estimate = cohort_1.size / cohort.size
        z_alpha = norm.ppf(1 - alpha)
        ic_lower = math.sin(math.asin(math.sqrt(p_estimate)) - z_alpha / (2 * math.sqrt(cohort.size))) ** 2
        ic_upper = math.sin(math.asin(math.sqrt(p_estimate)) + z_alpha / (2 * math.sqrt(cohort.size))) ** 2
    else:
        ic_lower, ic_upper = proportion_confint(cohort_1.size, cohort.size, alpha=alpha * 2, method=method_stat)
    return ic_lower, ic_upper

def simulation_binomial(cohort_size, num_simu, espilon, H0, alpha, method_stat):
    """Simulation processing.

    Args:
        cohort_size (int): cohort size.
        num_simu (int): Number of simulation for each run.
        espilon (float): Bernouilli parameter
        H0 (float): H0 hypothesis in bilateral conformation.
        alpha (float): alpha value
        method_stat (string): method to estimate benomial IC (cf compute_IC_binomial function).

    Returns:
        pandas dataframe: simulations data
    """
    results_simulation = {"simulation_ID": [], "IC_lower": [], "flag": [], "p_estimate": []}
    for i in range(num_simu):
        flag = None
        cohort = generate_cohorte_binom(1, espilon, cohort_size)
        ic_lower, ic_upper = compute_IC_binomial(cohort, alpha, method_stat)
        p_estimate = cohort[cohort == 1].size / cohort.size
        if ic_lower > H0:
            flag = 1
        else:
            flag = 0
        results_simulation["simulation_ID"].append(i)
        results_simulation["IC_lower"].append(ic_lower)
        results_simulation["flag"].append(flag)
        results_simulation["p_estimate"].append(p_estimate)
    results_simulation_data = pd.DataFrame(results_simulation)
    return results_simulation_data

def monte_carlo_process_binomial(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat):
    """Monte Carlo process

    Args:
        cohort_size_start (int): Maximal cohort size
        cohort_size_end (_type_): Minimal cohor size
        num_simu (int): Number of simulation for each run
        epsilon_H0 (float): proportion expected under H0 (bibliography result). Control alpha error. Control alpha error.
        epsilon_H1 (float): Proportion value under H1. Control beta error.
        H0 (float): H0 hypothesis in bilateral conformation.
        alpha (float): alpha value
        power (float): beta value
        method_stat (string): IC method name to estimate Binomial IC (cf compute_IC_binomial function).

    Returns:
        pandas dataframe: Monte Carlo simulation
    """
    global_time_start = time.time()
    data = {"alpha": [], "power": [], "size": [], "method":[], "time": [], "global_time": [], "simulation": [], "mse_alpha": [], "mse_power": []}
    cohort_size = cohort_size_start
    i = 1
    print("==== Simulation in progress ====")
    print("Method confidence interval: ", method_stat)
    while cohort_size >= cohort_size_end:
        start_time = time.time()
        sim1 = simulation_binomial(cohort_size, num_simu, epsilon_H0, H0, alpha, method_stat)
        sim2 = simulation_binomial(cohort_size, num_simu, epsilon_H1, H0, alpha, method_stat)
        alpha_found = sim1[sim1["flag"] == 1]["flag"].shape[0] / num_simu
        power_found = sim2[sim2["flag"] == 1]["flag"].shape[0] / num_simu
        alpha_found = round(alpha_found, 4)
        power_found = round(power_found, 4)
        mse_1 = np.sum((sim1["p_estimate"] - epsilon_H0) ** 2) / num_simu
        mse_2 = np.sum((sim2["p_estimate"] - epsilon_H1) ** 2) / num_simu
        end_time = time.time()
        total_time = round(end_time - start_time, 2)
        s = "[INFO] Step " + str(i) + "--- Sample size: " + str(cohort_size) + " | Alpha: " + str(alpha_found) + " | Power: " + str(power_found) + " | MSE_H0: " + str(mse_1) + " | MSE_H1: " + str(mse_2) + " (exec: " + str(total_time) + " s)" 
        print(s)
        data["alpha"].append(alpha_found)
        data["power"].append(power_found)
        data["size"].append(cohort_size)
        data["method"].append(method_stat)
        data["time"].append(total_time)
        data["simulation"].append(num_simu)
        data["mse_alpha"].append(mse_1)
        data["mse_power"].append(mse_2)
        i += 1
        cohort_size -= 1
    global_time_end = time.time()
    global_total_time = round(global_time_end - global_time_start, 2)
    global_time_list = [global_total_time for _ in range(len(data["alpha"]))]
    data["global_time"] = global_time_list
    print("Total execution: ", str(global_total_time), "secondes.")
    print("==== Simulation finished ===")
    data = pd.DataFrame(data)
    return data

def research_sample_size_optimal(data_simulation_monte_carlo, alpha, power):
    """Research of the best sample size 
    (minimum of patient with alpha and beta error controlled).

    Args:
        data_simulation_monte_carlo (pandas dataframe): data result of monte_carlo_process_binomial funtion.
        alpha (float): alpha value
        power (flaot): beta value

    Returns:
        pandas dataframe: all sample size retain.
    """
    return data_simulation_monte_carlo[(data_simulation_monte_carlo["alpha"] <= alpha) & (data_simulation_monte_carlo["power"] >= power)]

def api(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat):
    """API sample size, proportion test.

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

    Returns:
        pandas dataframe: Sample size respecting H0, H1 hypothesis and control of type I and II errors.
    """
    if type(cohort_size_start) != int:
        raise ValueError("cohort_size_start parameter must be integer.")
    if type(cohort_size_end) != int:
        raise ValueError("cohort_size_end parameter must be integer.")
    if type(num_simu) != int:
        raise ValueError("num_simu parameter must be integer.")
    if type(epsilon_H0) != float:
        raise ValueError("epsilon_H0 parameter must be integer.")
    if type(epsilon_H1) != float:
        raise ValueError("epsilon_H1 parameter must be integer.")
    if type(H0) != float:
        raise ValueError("H0 parameter must be integer.")
    if type(alpha) != float:
        raise ValueError("alpha parameter must be integer.")
    if type(power) != float:
        raise ValueError("power parameter must be integer.")
    if type(method_stat) != str:
        raise ValueError("method_stat parameter must be integer.")
    if method_stat not in ["normal", "beta", "wilson", "arcsinus"]:
        raise ValueError("Method to determine Binomial IC not found.\nPease choose one of these method: normal, beta, wilson, arcsinus.")
    if power > 1 or power < 0:
        raise ValueError("Power must be in [0, 1]")
    if alpha > 1 or alpha < 0:
        raise ValueError("Alpha must be in [0, 1]")
    if num_simu <= 1:
        raise ValueError("Number of simulation must be greater than 1.")
    if cohort_size_start <= 2:
        raise ValueError("Maximal cohort size must contain a number of patient greater than 2.")
    if cohort_size_start < 1:
        raise ValueError("Minimal cohort size must contain a number of patient greater than 1.")
    if epsilon_H0 > 1 or epsilon_H0 < 0:
        raise ValueError("epsilon_H0 must be in [0, 1]")
    if epsilon_H1 > 1 or epsilon_H1 < 0:
        raise ValueError("epsilon_H1 must be in [0, 1]")
    if H0 > 1 or H0 < 0:
        raise ValueError("H0 must be in [0, 1]")
    data_simulation_monte_carlo = monte_carlo_process_binomial(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat)
    results_sample_size = research_sample_size_optimal(data_simulation_monte_carlo, alpha, power)
    return results_sample_size






























