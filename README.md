# Project Overview

Sample size calculation is a fundamental step in the design of any clinical trial. The objective is to strike a balance between two core needs:

- **Ensuring sufficient statistical power**, by controlling Type [I](https://fr.wikipedia.org/wiki/Test_statistique#Risque_de_premi%C3%A8re_esp%C3%A8ce_et_confiance) and Type [II](https://fr.wikipedia.org/wiki/Test_statistique#Risque_de_deuxi%C3%A8me_esp%C3%A8ce_et_puissance) errors.  

- **Minimizing patient exposure** to experimental treatments during the trial phase.

With the rise of innovative therapies — particularly in oncology (e.g., immunotherapy) — and the growth of artificial intelligence, clinical questions have become more complex. This has led to increasingly sophisticated statistical hypotheses. As a result, **classical formulas** for sample size calculation are often no longer sufficient, and **simulation-based approaches** are now essential.

---

### Project Goal

This project introduces an **educational method for computing sample size** in **non-randomized Phase II clinical trials**, where the population follows a **binomial distribution**.

Developed by *Maxime Fleury* (biostatistician at the Biostatistics and Methodology Unit of the Paoli-Calmettes Institute), the tool offers three user-level approaches:

1. **Python 3 Terminal Mode**:  
     For quick simulations directly from the command line, with immediate results.

2. **IDE Execution (e.g., VS Code, PyCharm)**:  
     For users who want to fine-tune parameters, process data, or integrate simulation functions into their own code.

3. **Local GUI via Tkinter**:  
     A *user-friendly* desktop application that enables intuitive usage and helps users explore the logic behind the project.

---

This project can be found on the vignette (link to the vignette in progress), on GitLab and GitHub (link in progress).

## Installation

To install this project you must dispose of MacOS, Window 10 or linux distribution. Minimal informatics power and ressources are required (intel icore I5 for exemple). You must dispose of [git](https://git-scm.com/) and [anaconda](https://anaconda.org/anaconda/conda) in last version.

After, going to your desired directory where you want install this project and execute following command.

**1 Install project :**

```
git clone https://gitlab.com/F.MAXIME/sample_size_simulation.git
```

A file **sample_size_simulation** is created. Then going in this file with `cd sample_size_simulation`.

**2 Install environment :**

This project was programed in **python3** in version **3.10** with many packages. You can obtain the list of packages when you open `config_env.yml` file in **config** directory. To install the conda environment and all dependencies execute the following command in the **config**:

Install conda environment:

```
conda env create -f sample_size_simu_env.yml
```

3 Activate conda environment:

```
conda activate sample_size_simu_env
```

Desactivate conda environment:

```
conda deactivate
```

## Demo

> **The demonstration is based on the following scenario:**
>
> An experimental treatment (**TR1**) will be considered effective if at least **70%** of patients achieve a complete response at 2 years. According to the literature, an **80%** complete response rate is expected. Moreover, we suppose that patient distribution follow a Binomial low.

To realize the simulation and obtain the optimal sample size we use $\alpha = 0.05$ and $\beta = 0.2$. *Arcsinus* confidance interval estimation is used (reference to vignette LINK in progress) and the research of the **sample size must between 200 at 10 patients**.

> *Binomial interval confidence estimator* can be choosen in next method:
>
> - [Wilson](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Wilson_score_interval)
> 
> - [Beta](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Clopper%E2%80%93Pearson_interval)
> 
> - [Normal](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Problems_with_using_a_normal_approximation_or_%22Wald_interval%22)
> 
> - [Arcsinus](https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval#Arcsine_transformation)
>
> To compare different method performences, please refer to the web site (link in progress).


### Python 3 Terminal Mode

Open your terminal and execute the following command line to obtain a simulation sample size result

```
python3 run_simulation_terminal_job.py -start 200 -end 10 -NumSimu 1000 -epsilonH0 0.7 -epsilonH1 0.8 -H0 0.7 -alpha 0.05 -power 0.8 -method arcsinus
```

All simulations results are printed in the terminal and at the end the following table is printed.

| alpha | power | size | method   | time | global_time | simulation | mse_alpha  | mse_power  |
|-------|-------|------|----------|------|-------------|------------|------------|------------|
| 0.031 | 0.930 | 197  | arcsinus | 0.08 | 14.38       | 1000       | 0.00102126 | 0.00087585 |
| 0.043 | 0.944 | 194  | arcsinus | 0.08 | 14.38       | 1000       | 0.00109952 | 0.00080065 |
| 0.041 | 0.946 | 193  | arcsinus | 0.08 | 14.38       | 1000       | 0.00110124 | 0.00082251 |
| 0.049 | 0.923 | 190  | arcsinus | 0.08 | 14.38       | 1000       | 0.00110579 | 0.00086781 |
| 0.050 | 0.936 | 188  | arcsinus | 0.08 | 14.38       | 1000       | 0.00116913 | 0.00084337 |
| 0.041 | 0.937 | 185  | arcsinus | 0.08 | 14.38       | 1000       | 0.00104164 | 0.00086156 |
| 0.043 | 0.918 | 179  | arcsinus | 0.08 | 14.38       | 1000       | 0.00110532 | 0.00095197 |
| 0.045 | 0.927 | 178  | arcsinus | 0.08 | 14.38       | 1000       | 0.00114249 | 0.00089327 |
| 0.043 | 0.921 | 171  | arcsinus | 0.08 | 14.38       | 1000       | 0.00117478 | 0.00092150 |
| 0.048 | 0.916 | 170  | arcsinus | 0.08 | 14.38       | 1000       | 0.00113062 | 0.00094519 |
| 0.045 | 0.915 | 168  | arcsinus | 0.08 | 14.38       | 1000       | 0.00117041 | 0.00092949 |
| 0.042 | 0.915 | 167  | arcsinus | 0.08 | 14.38       | 1000       | 0.00116929 | 0.00093806 |
| 0.047 | 0.923 | 166  | arcsinus | 0.08 | 14.38       | 1000       | 0.00121067 | 0.00092582 |
| 0.050 | 0.940 | 161  | arcsinus | 0.08 | 14.38       | 1000       | 0.00126986 | 0.00093509 |
| 0.047 | 0.910 | 158  | arcsinus | 0.08 | 14.38       | 1000       | 0.00130337 | 0.00099102 |
| 0.038 | 0.877 | 153  | arcsinus | 0.08 | 14.38       | 1000       | 0.00144890 | 0.00108544 |
| 0.047 | 0.917 | 151  | arcsinus | 0.08 | 14.38       | 1000       | 0.00129249 | 0.00104089 |
| 0.039 | 0.881 | 149  | arcsinus | 0.08 | 14.38       | 1000       | 0.00148851 | 0.00115507 |
| 0.050 | 0.890 | 148  | arcsinus | 0.08 | 14.38       | 1000       | 0.00140944 | 0.00104022 |
| 0.042 | 0.849 | 146  | arcsinus | 0.08 | 14.38       | 1000       | 0.00147038 | 0.00119897 |
| 0.046 | 0.887 | 145  | arcsinus | 0.08 | 14.38       | 1000       | 0.00136200 | 0.00104656 |
| 0.027 | 0.862 | 142  | arcsinus | 0.08 | 14.38       | 1000       | 0.00147959 | 0.00109231 |
| 0.045 | 0.868 | 141  | arcsinus | 0.08 | 14.38       | 1000       | 0.00146928 | 0.00107488 |
| 0.049 | 0.843 | 137  | arcsinus | 0.08 | 14.38       | 1000       | 0.00146979 | 0.00128118 |
| 0.047 | 0.849 | 133  | arcsinus | 0.08 | 14.38       | 1000       | 0.00153956 | 0.00132509 |
| 0.043 | 0.830 | 131  | arcsinus | 0.08 | 14.38       | 1000       | 0.00165601 | 0.00114380 |
| 0.044 | 0.833 | 130  | arcsinus | 0.08 | 14.38       | 1000       | 0.00157882 | 0.00122036 |
| 0.043 | 0.828 | 127  | arcsinus | 0.08 | 14.38       | 1000       | 0.00162113 | 0.00120126 |
| 0.049 | 0.807 | 123  | arcsinus | 0.08 | 14.38       | 1000       | 0.00173804 | 0.00126107 |
| 0.049 | 0.807 | 122  | arcsinus | 0.08 | 14.38       | 1000       | 0.00180098 | 0.00129931 |
| 0.046 | 0.845 | 120  | arcsinus | 0.08 | 14.38       | 1000       | 0.00171958 | 0.00133764 |
| 0.047 | 0.821 | 119  | arcsinus | 0.08 | 14.38       | 1000       | 0.00176581 | 0.00140853 |
| 0.049 | 0.804 | 110  | arcsinus | 0.08 | 14.38       | 1000       | 0.00196802 | 0.00140256 |


This table represent all optimal sample size which respect statistical condition (type I and II error controlled under H0 and H1 hypothesis).

### IDE Execution (e.g., VS Code, PyCharm)

Open the script `run_simulation_MAIN.py` and adapt next parameters:

```
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
```

Then execute the code. In `data` variable you obtain the same resulst that in **Python 3 Terminal Mode** part and in the *OUTPUTS* file 3 graphics are obtain:

- Evolution of $\alpha$ in function of sample size

- Evolution of $\beta$ in function of sample size

- Evolution of MSE of $\alpha$ and $\beta$ estimate in function of sample size against $\alpha$ and $\beta$ computed by formula. 

### Local GUI via Tkinter

In your terminal execute the following command:

```
python3 run_simualtion_terminal_job.py
```

A tkinter window is open and you can adjust same parameters that in **IDE Execution** part. After parameters choose, click on *run simulation* and in the tabview **sample size results** you obtain optimal sample size table and in **graphics** you obtain graphics which study  $\alpha$, $\beta$ and MSE results in function of sample size.


## Acknowledgements

I would like to express my sincere gratitude to **Patrick Sfumato** and **Christophe Zemmour**,   members of the <i>Biostatistics and Methodology Unit of the Paoli-Calmettes Institute</i>, for their valuable support in understanding the **methodological** and **statistical** aspects of this project.

## Authors

- Maxime Fleury - Health data scientist / Biostatistician - Paoli-Calmettes Institut - Biostatistique and methodology Unit - FLEURYM@ipc.unicancer.fr

## DATE

This project was started 03/07/2025.

**Last documentation update:** 10/07/2025.

**Last program update:** 10/07/2025.

## LICENCE

<a href="https://creativecommons.org">Untitled</a> © 1999 by <a href="https://creativecommons.org">Jane Doe</a> is licensed under <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International</a><img src="https://mirrors.creativecommons.org/presskit/icons/cc.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/by.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/nc.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;"><img src="https://mirrors.creativecommons.org/presskit/icons/nd.svg" alt="" style="max-width: 1em;max-height:1em;margin-left: .2em;">



