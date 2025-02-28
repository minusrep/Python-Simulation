import customtkinter as ctk
from customtkinter import CTkTabview
from simulation import run_simulation_first_method, run_simulation_second_method, TrendAnalyzer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App:
    def __init__(self):
        self.setup_ui()
        self.setup_tabs()
        self.setup_default_values()
        self.setup_first_simulation_tab()
        self.setup_second_simulation_tab()
        self.setup_about_tab()

    def setup_ui(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Моделирование реле")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

    def setup_tabs(self):
        self.tabview = CTkTabview(self.root)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        self.tabview.add("Первая симуляция")
        self.tabview.add("Вторая симуляция")
        self.tabview.add("О программе")

    def setup_default_values(self):
        self.default_values_first = {
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
            "tmax": (0.3, "с"),  # Добавлено tmax
        }

        self.default_values_second = {
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
            "R1": (1000, "Ом"),
            "C": (0.019558982, "Ф"),
            "ΔU": (10, "В"),
            "tmax": (0.3, "с"),  # Добавлено tmax
        }

    def setup_first_simulation_tab(self):
        self.entries_first = {}  # Отдельный словарь для первой вкладки
        self.create_parameter_entries(self.tabview.tab("Первая симуляция"), self.default_values_first, self.entries_first)
        self.create_simulation_button(self.tabview.tab("Первая симуляция"), "Запустить первую симуляцию", self.start_first_simulation)

    def setup_second_simulation_tab(self):
        self.entries_second = {}  # Отдельный словарь для второй вкладки
        self.create_parameter_entries(self.tabview.tab("Вторая симуляция"), self.default_values_second, self.entries_second)
        self.create_simulation_button(self.tabview.tab("Вторая симуляция"), "Запустить вторую симуляцию", self.start_second_simulation)

    def create_parameter_entries(self, parent, default_values, entries_dict):
        params_frame = ctk.CTkFrame(parent)
        params_frame.pack(padx=10, pady=10, fill="x")

        for param, (value, unit) in default_values.items():
            self.create_parameter_row(params_frame, param, value, unit, entries_dict)

    def create_parameter_row(self, parent, param, value, unit, entries_dict):
        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(fill="x", padx=5, pady=2)

        label = ctk.CTkLabel(row_frame, text=f"{param}:", width=50, anchor="w")
        label.pack(side="left", padx=5)

        entry = ctk.CTkEntry(row_frame, width=150)
        entry.insert(0, str(value))
        entry.pack(side="left", padx=5)
        entries_dict[param] = entry  # Сохраняем ссылку на поле ввода в соответствующем словаре

        unit_label = ctk.CTkLabel(row_frame, text=unit)
        unit_label.pack(side="left", padx=5)

    def create_simulation_button(self, parent, text, command):
        button = ctk.CTkButton(parent, text=text, command=command)
        button.pack(pady=10)

    def setup_about_tab(self):
        label = ctk.CTkLabel(self.tabview.tab("О программе"), text="О программе: Моделирование реле")
        label.pack(padx=10, pady=10)

    def start_first_simulation(self):
        params = {param: float(entry.get()) for param, entry in self.entries_first.items()}
        self.show_simulation_results(params, run_simulation_first_method)

    def start_second_simulation(self):
        params = {param: float(entry.get()) for param, entry in self.entries_second.items()}
        self.show_simulation_results(params, run_simulation_second_method)

    def show_simulation_results(self, params, simulation_function):
        results = simulation_function(params)
        self.show_results_window(results, params["tmax"])

    def show_results_window(self, results, tmax):
        results_window = ctk.CTkToplevel(self.root)
        results_window.title("Результаты симуляции")
        results_window.geometry("1200x600")
        results_window.resizable(False, False)

        graph_frame = ctk.CTkFrame(results_window)
        graph_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        fig, ax = plt.subplots()
        ax.plot(results["time"], results["current"])
        ax.set_xlabel('Время (t)')
        ax.set_ylabel('Ток (i)')
        ax.set_title('Зависимость тока от времени')
        ax.grid(True)

        # Добавление аннотаций
        trend_analyzer = TrendAnalyzer(results["time"], results["current"])
        events = trend_analyzer.get_events()

        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

        trend_frame = ctk.CTkFrame(results_window)
        trend_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        trend_info = trend_analyzer.analyze_trends()

        text_box = ctk.CTkTextbox(trend_frame, wrap="word")
        text_box.insert("1.0", trend_info)
        text_box.configure(state="disabled")
        text_box.pack(fill="both", expand=True, padx=10, pady=10)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()