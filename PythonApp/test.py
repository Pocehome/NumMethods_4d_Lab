import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class SplineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spline Approximation")

        self.setup_ui()

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(control_frame, text="Отрезок [a, b]").pack()

        self.a_entry = tk.Entry(control_frame)
        self.a_entry.insert(0, "-1")
        self.a_entry.pack()

        self.b_entry = tk.Entry(control_frame)
        self.b_entry.insert(0, "1")
        self.b_entry.pack()

        tk.Label(control_frame, text="Граничные условия").pack()

        self.sa_entry = tk.Entry(control_frame)
        self.sa_entry.insert(0, "0")
        self.sa_entry.pack()

        self.sb_entry = tk.Entry(control_frame)
        self.sb_entry.insert(0, "0")
        self.sb_entry.pack()

        tk.Label(control_frame, text="Число разбиений").pack()
        self.split_num_entry = tk.Entry(control_frame)
        self.split_num_entry.insert(0, "100")
        self.split_num_entry.pack()

        self.approx_button = tk.Button(control_frame, text="Аппроксимировать", command=self.approximate)
        self.approx_button.pack()

        self.func_list = ttk.Combobox(control_frame,
                                      values=["Тестовая", "F(x) = sqrt(x^2-1)/x", "F(x) = (1+x^2)^(1/3)"])
        self.func_list.current(0)
        self.func_list.pack()

        self.create_plots()

    def create_plots(self):
        plot_frame = tk.Frame(self.root)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.axs = plt.subplots(1, 3, figsize=(9, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def approximate(self):
        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            n = int(self.split_num_entry.get())
            x = np.linspace(a, b, n)
            y = np.sin(x)  # Заглушка для теста

            for ax in self.axs:
                ax.clear()
                ax.plot(x, y)
                ax.set_title("Graph")

            self.canvas.draw()
        except ValueError:
            print("Invalid input")


if __name__ == "__main__":
    root = tk.Tk()
    app = SplineApp(root)
    root.mainloop()
