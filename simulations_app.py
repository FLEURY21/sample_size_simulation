__docformat__ = "google"
#############################################################################################
#| Program name: simulations_app.py                                                         #
#| Description: Application script                                                          #
#|                                                                                          #
#| Author: Maxime FLEURY - Institut Paoli Calmettes - Biostatistics and methodology Unit    #
#| Current programmer: Maxime Fleury                                                        #
#| Origine date: 8 July 2025                                                                #
#| Last modification: 8 July 2025                                                           #
#| Version: 1.0                                                                             #
#| Input (programs and data): simulations.py, graph_simulations.py                          #
#| Output (programs and data): None                                                         #
#############################################################################################

# Imports
#---------
from script.simulations import *
from script.generate_graph_simulations import *
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter
from typing import Union, Callable

# Class
#-------

class WidgetName(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

class FloatSpinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 width: int = 100,
                 height: int = 32,
                 step_size: Union[int, float] = 1,
                 command: Callable = None,
                 label_text: str = "Label:",
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.step_size = step_size
        self.command = command
        self.configure(fg_color="transparent")  
        self.grid_columnconfigure((0, 1, 3), weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.label = customtkinter.CTkLabel(self, text=label_text)
        self.label.grid(row=0, column=0, padx=(5, 3), pady=3)
        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                       command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=1, padx=(0, 0), pady=3)
        self.entry = customtkinter.CTkEntry(self, width=width - (3 * height), height=height-6, border_width=0)
        self.entry.grid(row=0, column=2, columnspan=1, padx=3, pady=3, sticky="ew")
        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                  command=self.add_button_callback)
        self.add_button.grid(row=0, column=3, padx=(0, 5), pady=3)
        self.entry.insert(0, "0.0")

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) + self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = float(self.entry.get()) - self.step_size
            self.entry.delete(0, "end")
            self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[float, None]:
        try:
            return float(self.entry.get())
        except ValueError:
            return None

    def set(self, value: float):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(float(value)))

# Function button
#-----------------

def display_dataframe_with_treeview(
        tab,
        dataframe: pd.DataFrame,
        header_fg: str = "steelblue",
        header_font=("Helvetica", 12, "bold")
    ):
    for widget in tab.winfo_children():
        widget.destroy()
    if dataframe.empty:
        customtkinter.CTkLabel(
            tab,
            text="Aucun résultat à afficher.",
            font=("Helvetica", 14)
        ).pack(padx=20, pady=20)
        return
    df = dataframe.copy()
    pretty_cols = [c.replace("_", " ").title() for c in df.columns]
    rename_map = dict(zip(df.columns, pretty_cols))
    df.columns = pretty_cols                     
    frame = tk.Frame(tab)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    yscroll = ttk.Scrollbar(frame, orient="vertical")
    yscroll.pack(side="right", fill="y")
    xscroll = ttk.Scrollbar(frame, orient="horizontal")
    xscroll.pack(side="bottom", fill="x")
    style = ttk.Style(frame)
    style.configure(
        "Custom.Treeview.Heading",
        font=header_font,
        foreground=header_fg
    )
    tree = ttk.Treeview(
        frame,
        columns=list(df.columns),
        show="headings",
        yscrollcommand=yscroll.set,
        xscrollcommand=xscroll.set,
        style="Custom.Treeview"
    )
    tree.pack(fill="both", expand=True)
    yscroll.config(command=tree.yview)
    xscroll.config(command=tree.xview)
    def col_width(col, default=80, pad=20):
        texts = [str(v) for v in df[col]]
        max_len = max([len(col)] + [len(t) for t in texts])
        return max(default, max_len * 7 + pad)
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=col_width(col))
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))
    def sort_by(col, descending):
        data = [(tree.set(k, col), k) for k in tree.get_children("")]
        try:
            data = [(float(text), k) for text, k in data]
        except ValueError:
            pass
        data.sort(reverse=descending)
        for idx, (_, k) in enumerate(data):
            tree.move(k, "", idx)
        tree.heading(col, command=lambda: sort_by(col, not descending))
    for col in df.columns:
        tree.heading(col, command=lambda c=col: sort_by(c, False))

def display_carousel_of_figures(tab, figures):
    for widget in tab.winfo_children():
        widget.destroy()

    current_index = tk.IntVar(value=0)
    def show_figure(index):
        for widget in figure_frame.winfo_children():
            widget.destroy()

        fig = figures[index]
        canvas = FigureCanvasTkAgg(fig, master=figure_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()
    def next_figure():
        i = current_index.get()
        if i < len(figures) - 1:
            current_index.set(i + 1)
            show_figure(current_index.get())
    def prev_figure():
        i = current_index.get()
        if i > 0:
            current_index.set(i - 1)
            show_figure(current_index.get())
    nav_frame = tk.Frame(tab)
    nav_frame.pack(pady=10)
    btn_prev = tk.Button(nav_frame, text="← Précédent", command=prev_figure)
    btn_prev.grid(row=0, column=0, padx=10)
    btn_next = tk.Button(nav_frame, text="Suivant →", command=next_figure)
    btn_next.grid(row=0, column=1, padx=10)
    figure_frame = tk.Frame(tab)
    figure_frame.pack(fill="both", expand=True)
    show_figure(current_index.get())


def run_simulation_callback(output_tabs_list, cohort_size_start_param, cohort_size_end_param, num_simu_param, epsilon_H0_param, epsilon_H1_param, H0_param, alpha_param, beta_param, method_stat_param):
    cohort_size_start = int(cohort_size_start_param.get())
    cohort_size_end = int(cohort_size_end_param.get())
    num_simu = int(num_simu_param.get())
    epsilon_H0 = float(epsilon_H0_param.get())
    epsilon_H1 = float(epsilon_H1_param.get())
    H0 = float(H0_param.get())
    alpha = float(alpha_param.get())
    power = 1 - float(beta_param.get())
    method_stat = str(method_stat_param.get())
    data = api(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat)
    data["mse_power"] = data["mse_power"].round(5)
    data["mse_alpha"] = data["mse_alpha"].round(5)
    display_dataframe_with_treeview(output_tabs_list[0], data)
    f1, f2, f3 = graph_api(cohort_size_start, cohort_size_end, num_simu, epsilon_H0, epsilon_H1, H0, alpha, power, method_stat, output_path="no save")
    display_carousel_of_figures(output_tabs_list[1], [f1, f2, f3])


#-------------#
# APP program #
#-------------#
        
# ==== CONSTANTES DESIGN ====

# Window app constante
title_app = "My app"
size_x = 1080
size_y = 1080


# frame constante coord
frame_parameter_simu_width = 290
frame_parameter_simu_heigth = 190

frame_parameter_stat_width = 290
frame_parameter_stat_heigth = 220

label_width_simu = frame_parameter_simu_width
label_heigth_simu = 50

label_width_stat = frame_parameter_stat_width
label_heigth_stat = 50

coord_x_label_simu = 10
coor_y_label_simu = 40

coord_x_frame_simu = coord_x_label_simu
coord_y_frame_simu = label_heigth_simu + 50

coord_x_label_stat = 10
coor_y_label_stat = frame_parameter_simu_heigth + 130

coord_x_frame_stat = coord_x_label_stat
coord_y_frame_stat = coor_y_label_stat + 60

parameters_dy = 35
parameters_dx = 0

parameter_x_start = 10
parameter_y_start = 0

# frame text
simu_title_param = "Simulation parameters"
stat_title_param = "Statistics parameters"

police_title_param = "Helvetica"
size_police_title_param = 20

# output
output_width = 800
output_height = 900

output_x_coord = max(frame_parameter_simu_width, frame_parameter_stat_width) + 50
output_y_coord = 22

tab1_output_title = "Sample size found"
tab2_output_title = "Graphics"

# spinbox
spinbox_width = 150

# buttons
## simulation run
coor_x_run_simu_button = frame_parameter_stat_width / 4
coor_y_run_simu_button = coord_y_frame_stat + frame_parameter_stat_heigth + 50
label_text_button_run_simu = "Run simulations"


# ==== Window APP parameters ====
app = customtkinter.CTk()
app.title(title_app)
app.geometry(str(size_x) + "x" + str(size_y))

# ==== Frames APP ====

## labels title parameters frame
#--------------------------------

# style
font_style = customtkinter.CTkFont(family=police_title_param, size=size_police_title_param, weight="bold", underline=True)

# Simulation
label_frame_param = customtkinter.CTkFrame(master=app, width=label_width_simu, height=label_heigth_simu)
label_frame_param.place(x=coord_x_label_simu, y=coor_y_label_simu)
label = customtkinter.CTkLabel(label_frame_param, text=simu_title_param, font=font_style)
label.place(relx=0.5, rely=0.5, anchor="center")

# Statistics
label_frame_stats = customtkinter.CTkFrame(master=app, width=label_width_stat, height=label_heigth_stat)
label_frame_stats.place(x=coord_x_label_stat, y=coor_y_label_stat)
label2 = customtkinter.CTkLabel(label_frame_stats, text=stat_title_param, font=font_style)
label2.place(relx=0.5, rely=0.5, anchor="center")  

## Parameters frame
#-------------------

#Simulation
simulation_param_frame = customtkinter.CTkFrame(master=app, width=frame_parameter_simu_width, height=frame_parameter_simu_heigth)
simulation_param_frame.place(x=coord_x_frame_simu, y=coord_y_frame_simu)

# Statitics 
statistic_param_frame = customtkinter.CTkFrame(master=app, width=frame_parameter_stat_width, height=frame_parameter_stat_heigth)
statistic_param_frame.place(x=coord_x_frame_stat, y=coord_y_frame_stat)

# Output frame (tab view)
tab_output = customtkinter.CTkTabview(app, width=output_width, height=output_height)
tab_output.place(x=output_x_coord, y=output_y_coord)
tab1 = tab_output.add(tab1_output_title)
tab2 = tab_output.add(tab2_output_title)


# ==== Parameters ====

## Disign and frame organization
#-------------------------------

# Cohort_size_start
cohort_size_start_button = FloatSpinbox(master=simulation_param_frame, width=spinbox_width, step_size=1, label_text="Maximal cohort size:   ")
cohort_size_start_button.set(200)
cohort_size_start_button.place(x=parameter_x_start, y=parameter_y_start)
place_x = parameter_x_start
place_y = parameter_y_start


# Cohort_size_end
cohort_size_end_button = FloatSpinbox(master=simulation_param_frame, width=spinbox_width, step_size=1, label_text="Minimal cohort size:    ")
cohort_size_end_button.set(10)
cohort_size_end_button.place(x=place_x + parameters_dx, y=place_y + parameters_dy)
place_x = place_x + parameters_dx
place_y = place_y + parameters_dy


# Number of simulations
nb_simulation_button = FloatSpinbox(master=simulation_param_frame, width=spinbox_width, step_size=10, label_text="Number of simulation:")
nb_simulation_button.set(1000)
nb_simulation_button.place(x=place_x + parameters_dx, y=place_y + parameters_dy)
place_x = place_x + parameters_dx
place_y = place_y + parameters_dy


# simulation method
method_label = customtkinter.CTkLabel(simulation_param_frame, text="Confidence interval method:")
method_label.place(x=place_x + parameters_dx, y=place_y + parameters_dy) 
place_x = place_x + parameters_dx
place_y = place_y + parameters_dy
method_list = ["arcsinus", "beta", "wilson", "normal"]
combo_box_method_button = customtkinter.CTkComboBox(simulation_param_frame, values=method_list, button_color="red")
combo_box_method_button.place(x=place_x + (frame_parameter_simu_width / 4), y=place_y + parameters_dy)


# H0 hypothesis
H0_hypo_button = FloatSpinbox(master=statistic_param_frame, width=spinbox_width, step_size=0.01, label_text="H0 hypothesis:                  ")
H0_hypo_button.set(0.05)
H0_hypo_button.place(x=parameter_x_start, y=parameter_y_start)
place_x = parameter_x_start
place_y = parameter_y_start


# H0 expected value
H0_exp_hypo_button = FloatSpinbox(master=statistic_param_frame, width=spinbox_width, step_size=0.01, label_text="Expected value under H0:")
H0_exp_hypo_button.set(0.05)
H0_exp_hypo_button.place(x=parameter_x_start + parameters_dx, y=parameter_y_start + parameters_dy)
place_x = place_x + parameters_dx
place_y = place_y + parameters_dy


# H1 expected value
H1_hypo_button = FloatSpinbox(master=statistic_param_frame, width=spinbox_width, step_size=0.01, label_text="Expected value under H1:")
H1_hypo_button.set(0.05)
H1_hypo_button.place(x=place_x + parameters_dx, y=place_y + parameters_dy)
place_x = place_x + parameters_dx
place_y = place_y + parameters_dy


# alpha
alpha_button = FloatSpinbox(master=statistic_param_frame, width=spinbox_width, step_size=0.001, label_text="alpha:                                 ")
alpha_button.set(0.05)
alpha_button.place(x=place_x + parameters_dx, y=place_y + parameters_dy)
place_x = place_x + parameters_dx
place_y = place_y + parameters_dy


# beta
beta_button = FloatSpinbox(master=statistic_param_frame, width=spinbox_width, step_size=0.01, label_text="beta:                                   ")
beta_button.set(0.05)
beta_button.place(x=place_x + parameters_dx, y=place_y + parameters_dy)
place_x = place_x + parameters_dx
place_y = place_y + parameters_dy

# ==== BUTTON ACTION ====

run_button_simulation = customtkinter.CTkButton(app, text=label_text_button_run_simu, command=lambda: run_simulation_callback(
    [tab1, tab2],
    cohort_size_start_button,
    cohort_size_end_button,
    nb_simulation_button,
    H0_exp_hypo_button,
    H1_hypo_button,
    H0_hypo_button,
    alpha_button,
    beta_button,
    combo_box_method_button
))

run_button_simulation.place(x=coor_x_run_simu_button, y=coor_y_run_simu_button)


# ==== ROOT PROCESS ====

app.mainloop()




