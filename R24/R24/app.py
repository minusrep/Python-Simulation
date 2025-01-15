import customtkinter as ctk
from simulation import run_simulation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class App:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Ввод параметров")
        self.root.geometry("320x580")
        self.root.resizable(False, False)

        self.default_values = {
            "U": (50, "В"),
            "R": (5000, "Ом"),
            "W": (11500, ""),
            "D": (0.03, "м"),
            "δ0": (1.0e-3, "м"),
            "δk": (0.5e-3, "м"),
            "m": (2e-3, "кг"),
            "Fнач": (4, "Н"),
            "M": (4e3, "Н·м"),
            "dt": (1e-3, "с"),
        }

        self.create_widgets()

    def create_widgets(self):
        self.params_frame = ctk.CTkFrame(self.root)
        self.params_frame.pack(padx=10, pady=10, fill="x")

        self.entries = {}
        for param, (value, unit) in self.default_values.items():
            row_frame = ctk.CTkFrame(self.params_frame)
            row_frame.pack(fill="x", padx=5, pady=2)

            label = ctk.CTkLabel(row_frame, text=f"{param}:", width=50, anchor="w")
            label.pack(side="left", padx=5)

            entry = ctk.CTkEntry(row_frame, width=150)
            entry.insert(0, str(value))
            entry.pack(side="left", padx=5)
            self.entries[param] = entry

            unit_label = ctk.CTkLabel(row_frame, text=unit)
            unit_label.pack(side="left", padx=5)

        # Создаем раскрывающийся фрейм для выбора графиков
        self.plot_selection_frame = ctk.CTkFrame(self.root)
        self.plot_selection_frame.pack(padx=10, pady=10, fill="x")

        self.plot_selection_button = ctk.CTkButton(
            self.plot_selection_frame,
            text="Выбор графиков",
            command=self.toggle_plot_selection,
        )
        self.plot_selection_button.pack(fill="x")

        self.plot_selection_inner_frame = ctk.CTkFrame(self.plot_selection_frame)
        self.plot_selection_inner_frame.pack(fill="x", padx=5, pady=5)
        self.plot_selection_visible = False

        self.checkboxes = {
            "current": ctk.CTkCheckBox(self.plot_selection_inner_frame, text="Ток (i(t))"),
            "tau": ctk.CTkCheckBox(self.plot_selection_inner_frame, text="τ(t)"),
            "Fe": ctk.CTkCheckBox(self.plot_selection_inner_frame, text="Fэ(t)"),
            "Fm": ctk.CTkCheckBox(self.plot_selection_inner_frame, text="Fм(t)"),
            "delta": ctk.CTkCheckBox(self.plot_selection_inner_frame, text="δ(t)"),
            "inductance": ctk.CTkCheckBox(self.plot_selection_inner_frame, text="L(t)"),
        }

        for checkbox in self.checkboxes.values():
            checkbox.pack(pady=2)

        # Скрываем внутренний фрейм с чекбоксами по умолчанию
        self.plot_selection_inner_frame.pack_forget()

        self.button = ctk.CTkButton(self.root, text="Запустить симуляцию", command=self.start_simulation)
        self.button.pack(pady=10)

    def toggle_plot_selection(self):
        """Переключает видимость фрейма с выбором графиков."""
        if self.plot_selection_visible:
            self.plot_selection_inner_frame.pack_forget()
            self.plot_selection_visible = False
        else:
            self.plot_selection_inner_frame.pack(fill="x", padx=5, pady=5)
            self.plot_selection_visible = True

    def start_simulation(self):
        params = {param: float(entry.get()) for param, entry in self.entries.items()}
        self.show_simulation_results(params)

    def show_simulation_results(self, params):
        self.graph_window = ctk.CTkToplevel(self.root)
        self.graph_window.title("Результаты симуляции")
        self.graph_window.geometry("800x600")

        results = run_simulation(params)

        plt.style.use('dark_background')
        background_color = '#242424'
        text_color = 'white'
        grid_color = '#555555'

        selected_plots = [key for key, checkbox in self.checkboxes.items() if checkbox.get() == 1]
        num_plots = len(selected_plots)

        if num_plots == 0:
            return

        rows = (num_plots + 1) // 2
        cols = 2 if num_plots > 1 else 1
        fig, axes = plt.subplots(rows, cols, figsize=(12, 6 * rows / 2))
        fig.suptitle('Результаты симуляции', fontsize=16, color=text_color)
        fig.patch.set_facecolor(background_color)

        # Если axes не является массивом, преобразуем его в массив
        if num_plots == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes.reshape(1, -1)  # Преобразуем в двумерный массив, если одна строка

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        plot_data = {
            "current": ("Ток (i)", results["current"]),
            "tau": ("τ", results["tau"]),
            "Fe": ("Fэ", results["Fe"]),
            "Fm": ("Fм", results["Fm"]),
            "delta": ("δ", results["delta"]),
            "inductance": ("L", results["inductance"]),
        }

        for i, key in enumerate(selected_plots):
            if rows == 1 and cols == 1:
                ax = axes[i]
            else:
                ax = axes[i // cols][i % cols]  # Обращение к подграфикам в двумерном массиве

            title, data = plot_data[key]
            ax.plot(results["time"], data, color=colors[i])
            ax.set_xlabel('Время (t)', color=text_color)
            ax.set_ylabel(title, color=text_color)
            ax.set_title(f'Зависимость {title} от времени', color=text_color)
            ax.grid(True, color=grid_color)
            ax.set_facecolor(background_color)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

        # Создаем панель инструментов и изменяем ее цвет
        toolbar = NavigationToolbar2Tk(canvas, self.graph_window)
        toolbar.update()

        # Изменяем цвет нижней панели на #202020
        toolbar_frame = toolbar.winfo_children()[0]
        toolbar_frame.configure(background="#202020")

        canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()