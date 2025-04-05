import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import log10
from Lab_Spline_Module import Solver, MODE


class Window:
    def __init__(self, master):
        # variables
        self.solve_mode = MODE.TEST
        self.table_mode = 1
        self.graph_mode = 1
        self.nodes_num = None
        self.solver = None
        self.table_data = None

        # window master
        self.master = master
        self.master.title("Лабораторная работа №4")
        self.master.geometry("1300x600")

        # Виджет выбора типа задачи
        self.solve_mode_label = tk.Label(self.master, text="Выберите тип задачи:")
        self.solve_mode_label.grid(row=0, column=0, sticky='w')
        # Dropdown for mode selection
        self.solve_mode_selector = ttk.Combobox(self.master, values=["Тестовая", "1 вариант", "2 вариант",
                                                               "3 вариант", "4 вариант", "Осциллирующая"])
        self.solve_mode_selector.grid(row=1, column=0, sticky='we')
        self.solve_mode_selector.set("Тестовая")
        self.solve_mode_selector.bind("<<ComboboxSelected>>", self.on_solve_mode_selected)

        # Виджет выбора типа таблицы
        self.table_mode_label = tk.Label(self.master, text="Выберите таблицу:")
        self.table_mode_label.grid(row=2, column=0, sticky='w')
        # Dropdown for table mode selection
        self.table_mode_selector = ttk.Combobox(self.master, values=["Таблица 1", "Таблица 2", "Таблица 3"])
        self.table_mode_selector.grid(row=3, column=0, sticky='we')
        self.table_mode_selector.set("Таблица 1")
        self.table_mode_selector.bind("<<ComboboxSelected>>", self.on_table_mode_selected)

        # Виджет выбора типа графика
        self.graph_mode_label = tk.Label(self.master, text="Выберите график:")
        self.graph_mode_label.grid(row=4, column=0, sticky='w')
        # Dropdown for table mode selection
        self.graph_mode_selector = ttk.Combobox(self.master, values=["F(x) и S(x)", "F'(x) и S'(x)",
                                                                     "F''(x) и S''(x)", "Погрешности"])
        self.graph_mode_selector.grid(row=5, column=0, sticky='we')
        self.graph_mode_selector.set("F(x) и S(x)")
        self.graph_mode_selector.bind("<<ComboboxSelected>>", self.on_graph_mode_selected)

        # Calculate button
        self.calc_button = tk.Button(self.master, text="Вычислить", command=self.calculate)
        self.calc_button.grid(row=1, column=1, sticky='we')

        # Calculate button
        self.update_table_button = tk.Button(self.master, text="Построить таблицу", command=self.update_table)
        self.update_table_button.grid(row=3, column=1, sticky='we')

        # Calculate button
        self.update_plot_button = tk.Button(self.master, text="Построить график", command=self.update_plot)
        self.update_plot_button.grid(row=5, column=1, sticky='we')

        # Input fields for test task
        self.count_of_otr = tk.Label(self.master, text="Кол-во отрезков:")
        self.count_of_otr.grid(row=6, column=0, sticky='e')

        # Input fields
        self.entry_nodes_num = tk.Entry(self.master)

        # Set default values
        self.entry_nodes_num.insert(0, "100")

        # Placement of input fields
        self.entry_nodes_num.grid(row=6, column=1, sticky='ew')

        # Display widgets for "Тестовая задача" by default
        self.create_widgets()

    def on_solve_mode_selected(self, event):
        selected_mode = self.solve_mode_selector.get()
        self.clear_widgets()

        # Choose which widgets to display based on selected task
        if selected_mode == "Тестовая":
            self.solve_mode = MODE.TEST
        elif selected_mode == "1 вариант":
            self.solve_mode = MODE.Main1
        elif selected_mode == "2 вариант":
            self.solve_mode = MODE.Main2
        elif selected_mode == "3 вариант":
            self.solve_mode = MODE.Main3
        elif selected_mode == "4 вариант":
            self.solve_mode = MODE.Main4
        elif selected_mode == "Осциллирующая":
            self.solve_mode = MODE.OSC

        self.create_widgets()

    def on_table_mode_selected(self, event):
        selected_mode = self.table_mode_selector.get()

        # Choose which widgets to display based on selected task
        if selected_mode == "Таблица 1":
            self.table_mode = 1
        elif selected_mode == "Таблица 2":
            self.table_mode = 2
        elif selected_mode == "Таблица 3":
            self.table_mode = 3

    def on_graph_mode_selected(self, event):
        selected_mode = self.graph_mode_selector.get()

        # Choose which widgets to display based on selected task
        if selected_mode == "F(x) и S(x)":
            self.graph_mode = 1
        elif selected_mode == "F'(x) и S'(x)":
            self.graph_mode = 2
        elif selected_mode == "F''(x) и S''(x)":
            self.graph_mode = 3
        elif selected_mode == "Погрешности":
            self.graph_mode = 4

    def clear_widgets(self):
        # Remove all widgets except the dropdown
        for widget in self.master.winfo_children():
            if widget not in [self.solve_mode_selector, self.solve_mode_label,
                              self.table_mode_selector, self.table_mode_label,
                              self.graph_mode_selector, self.graph_mode_label,
                              self.calc_button, self.update_table_button, self.update_plot_button,
                              self.count_of_otr, self.entry_nodes_num]:
                widget.destroy()

        # Clear variables
        self.nodes_num = None
        self.solver = None
        self.table_data = None

    def create_widgets(self):
        self.master.grid_columnconfigure(0, weight=100)
        self.master.grid_columnconfigure(1, weight=2)
        self.master.grid_columnconfigure(2, weight=2)
        self.master.grid_columnconfigure(3, weight=2)

        # Create Treeview to display the table
        self.table = ttk.Treeview(self.master, columns=["Col" + str(i) for i in range(5)], show="headings")
        self.table.grid(row=7, rowspan=2, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)

        # Add horizontal and vertical scrolling
        vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.table.yview)
        vsb.grid(row=7, column=2, sticky='sne', rowspan=3)
        self.table.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.master, orient="horizontal", command=self.table.xview)
        hsb.grid(row=9, column=0, columnspan=3, sticky='esw')
        self.table.configure(xscrollcommand=hsb.set)

        # Configure stretching
        self.master.grid_rowconfigure(8, weight=1)  # Allows the table to expand vertically
        self.master.grid_columnconfigure(0, weight=1)  # Allows the table to expand horizontally

        # Create figure for the plot
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=6, column=4, rowspan=5, sticky='nse', padx=5, pady=5)

        # Create a Text widget for final report
        self.final_report_text = tk.Text(self.master, height=10, width=50)
        self.final_report_text.grid(row=0, column=4, rowspan=7, sticky='nwe', padx=5, pady=5)

    # def create_main1_mode_widgets(self):
    #     self.master.grid_columnconfigure(0, weight=100)
    #     self.master.grid_columnconfigure(1, weight=2)
    #     self.master.grid_columnconfigure(2, weight=2)
    #     self.master.grid_columnconfigure(3, weight=2)
    #
    #     # Input fields for test task
    #     tk.Label(self.master, text="Кол-во узлов:").grid(row=6, column=0, sticky='e')
    #
    #     # Input fields
    #     self.entry_nodes_num = tk.Entry(self.master)
    #
    #     # Set default values
    #     self.entry_nodes_num.insert(0, "100")
    #
    #     # Placement of input fields
    #     self.entry_nodes_num.grid(row=6, column=1, sticky='ew')
    #
    #     # Create Treeview to display the table
    #     self.table = ttk.Treeview(self.master, columns=["Col" + str(i) for i in range(5)], show="headings")
    #     self.table.grid(row=7, rowspan=2, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
    #
    #     # Add horizontal and vertical scrolling
    #     vsb = ttk.Scrollbar(self.master, orient="vertical", command=self.table.yview)
    #     vsb.grid(row=7, column=2, sticky='sne', rowspan=3)
    #     self.table.configure(yscrollcommand=vsb.set)
    #
    #     hsb = ttk.Scrollbar(self.master, orient="horizontal", command=self.table.xview)
    #     hsb.grid(row=9, column=0, columnspan=3, sticky='esw')
    #     self.table.configure(xscrollcommand=hsb.set)
    #
    #     # Configure stretching
    #     self.master.grid_rowconfigure(8, weight=1)  # Allows the table to expand vertically
    #     self.master.grid_columnconfigure(0, weight=1)  # Allows the table to expand horizontally
    #
    #     # Create figure for the plot
    #     self.figure = Figure(figsize=(6, 4), dpi=100)
    #     self.ax = self.figure.add_subplot(111)
    #     self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
    #     self.canvas.get_tk_widget().grid(row=5, column=4, rowspan=6, sticky='nse', padx=5, pady=5)
    #
    #     # Create a Text widget for final report
    #     self.final_report_text = tk.Text(self.master, height=10, width=50)
    #     self.final_report_text.grid(row=0, column=4, rowspan=7, sticky='nwe', padx=5, pady=5)

    def calculate(self):
        try:
            # Get values from input fields
            self.nodes_num = int(self.entry_nodes_num.get())

            # Checks for correctness of values
            if self.nodes_num <= 1:
                messagebox.showerror("Ошибка", "Количество узлов должно быть больше 1.")
                return

            # Solving based on selected item in ComboBox
            self.solver = Solver(self.nodes_num, self.solve_mode)
            self.solver.Solve()

            self.Xn = self.solver.getX_for_coef_table()
            self.A = self.solver.getA()
            self.B = self.solver.getB()
            self.C = self.solver.getC()
            self.D = self.solver.getD()

            self.XN = self.solver.getX()
            self.F = self.solver.getF()
            if self.solve_mode == MODE.TEST:
                self.F[-1] = 2.
            self.S = self.solver.getS()
            self.div_FS = [abs(self.F[i]-self.S[i]) for i in range(len(self.XN))]
            self.dF = self.solver.getDF()
            self.dS = self.solver.getDS()
            self.div_dFS = [abs(self.dF[i]-self.dS[i]) for i in range(len(self.XN))]

            self.ddF = self.solver.getD2F()
            self.ddS = self.solver.getD2S()
            self.div_ddFS = [abs(self.ddF[i]-self.ddS[i]) for i in range(len(self.XN))]

            self.update_table()
            self.update_plot()
            self.show_final_reference()

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения.")

    def update_table(self):
        # Clear Treeview before updating
        for row in self.table.get_children():
            self.table.delete(row)

        # Set column headers
        if self.table_mode == 1:
            columns = ["i", "Xi-1", "Xi", "Ai", "Bi", "Ci", "Di"]
            arr_width = [50, 100, 100, 100, 100, 100, 100]
        elif self.table_mode == 2:
            columns = ["i", "Xi", "F(x)", "S(x)", "F(x)-S(x)", "F'(x)", "S'(x)", "F'(x)-S'(x)"]
            arr_width = [50, 100, 100, 100, 100, 100, 100, 100]
        elif self.table_mode == 3:
            columns = ["i", "Xi", "F''(x)", "S''(x)", "F''(x)-S''(x)"]
            arr_width = [50, 100, 100, 100, 100]

        # Make table data
        if self.table_mode == 1:
            self.table_data = [[1, 0., 0., 0., 0., 0., 0.]] * (len(self.Xn) - 1)
            for i in range(len(self.Xn) - 1):
                self.table_data[i] = [i + 1, self.Xn[i], self.Xn[i + 1], self.A[i], self.B[i], self.C[i], self.D[i]]

        elif self.table_mode == 2:
            self.table_data = [[1, 0., 0., 0., 0., 0., 0., 0.]] * len(self.XN)
            # print(self.XN)
            for i in range(len(self.XN)):
                self.table_data[i] = [i, self.XN[i], self.F[i], self.S[i], self.div_FS[i],
                                      self.dF[i], self.dS[i], self.div_dFS[i]]

        elif self.table_mode == 3:
            self.table_data = [[1, 0., 0., 0., 0.]] * len(self.XN)
            for i in range(len(self.XN)):
                self.table_data[i] = [i, self.XN[i], self.ddF[i], self.ddS[i], self.div_ddFS[i]]

        # rename table columns
        if list(self.table["columns"]) != columns:
            self.table["columns"] = columns
            for i in range(len(columns)):
                self.table.heading(columns[i], text=columns[i])
                self.table.column(columns[i], width=arr_width[i], minwidth=arr_width[i])  # Set column width

        # Add data to the table with formatting
        for row in self.table_data:
            formatted_row = [f"{value:.6g}" if isinstance(value, float) else value for value in row]
            self.table.insert("", "end", values=formatted_row)

    def update_plot(self):
        # Clearing the graph
        self.ax.clear()

        if self.graph_mode == 1:
            self.plot_graph_FS()
        elif self.graph_mode == 2:
            self.plot_graph_dFS()
        elif self.graph_mode == 3:
            self.plot_graph_ddFS()
        elif self.graph_mode == 4:
            self.plot_graph_divs()

        # Customize the plot
        self.ax.set_xlabel('X')
        # self.ax.xaxis.set_tick_params(labelsize=8)
        # self.ax.yaxis.set_tick_params(labelsize=8)
        self.ax.legend()
        self.ax.grid()

        # Автоматическая настройка размещения элементов графика
        self.ax.figure.tight_layout()

        # Update the plot
        self.canvas.draw()

    def plot_graph_FS(self):
        self.ax.plot(self.XN, self.F, label=f'F(x)', color='blue', alpha=0.7)
        self.ax.plot(self.XN, self.S, label=f'S(x)', color='red', alpha=0.7)

    def plot_graph_dFS(self):
        self.ax.plot(self.XN, self.dF, label=f"F'(x)", color='blue', alpha=0.7)
        self.ax.plot(self.XN, self.dS, label=f"S'(x)", color='red', alpha=0.7)

    def plot_graph_ddFS(self):
        self.ax.plot(self.XN, self.ddF, label=f"F''(x)", color='blue', alpha=0.7)
        self.ax.plot(self.XN, self.ddS, label=f"S''(x)", color='red', alpha=0.7)

    def plot_graph_divs(self):
        self.ax.plot(self.XN, self.div_FS, label=f"|F(x)-S(x)|", color='blue', alpha=0.7)
        self.ax.plot(self.XN, self.div_dFS, label=f"|F'(x)-S'(x)|", color='red', alpha=0.7)
        self.ax.plot(self.XN, self.div_ddFS, label=f"|F''(x)-S''(x)|", color='darkgreen', alpha=0.7)

    def show_final_reference(self):
        # Clear the previous report text
        self.final_report_text.delete(1.0, tk.END)

        max_div_FS = max(self.div_FS)
        x_max_div_FS = self.XN[self.div_FS.index(max_div_FS)]
        max_div_dFS = max(self.div_dFS)
        x_max_div_dFS = self.XN[self.div_dFS.index(max_div_dFS)]
        max_div_ddFS = max(self.div_ddFS)
        x_max_div_ddFS = self.XN[self.div_ddFS.index(max_div_ddFS)]

        info = (
            f"Сетка сплайна: n = {self.solver.get_n_step()}\n"
            f"Контрольная сетка: N = {self.solver.get_N_step()}\n"
            f"Погрешность сплайна на контрольной сетке\n"
            f"max|F(x)-S(x)| = {max_div_FS:.9f} при x = {x_max_div_FS:.6f}\n"
            f"Погрешность производной на контрольной сетке\n"
            f"max|F'(x)-S'(x)| = {max_div_dFS:.9f} при x = {x_max_div_dFS:.6f}\n"
            f"Погрешность второй производной на контрольной сетке\n"
            f"max|F''(x)-S''(x)| = {max_div_ddFS:.9f} при x = {x_max_div_ddFS:.6f}\n"
        )

        self.final_report_text.insert(tk.END, info)


def create_gui():
    root = tk.Tk()
    app = Window(root)
    root.mainloop()


def print_table(table):
    for i in table:
        for j in i:
            # print(str(j).ljust(20), end="\t")
            print(j, end="\t")

        print()


if __name__ == "__main__":
    create_gui()
