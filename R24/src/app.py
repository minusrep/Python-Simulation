import customtkinter as ctk
from customtkinter import CTkTabview
from simulation import run_simulation_first_method, run_simulation_second_method, TrendAnalyzer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class App:
    def __init__(self):
        self.setup_ui()
        self.setup_tabs()
        self.setup_default_values()
        self.setup_first_simulation_tab()
        self.setup_second_simulation_tab()
        self.setup_about_tab()

    def setup_ui(self):
        """Настройка основного интерфейса приложения."""
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Моделирование реле")
        self.root.geometry("100%100%")  # Увеличим ширину окна для текстового поля
        self.root.resizable(False, False)

    def setup_tabs(self):
        """Создание вкладок."""
        self.tabview = CTkTabview(self.root)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        self.tabview.add("Первая симуляция")
        self.tabview.add("Вторая симуляция")
        self.tabview.add("О программе")

    def setup_default_values(self):
        """Установка значений по умолчанию для параметров."""
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
        }

    def setup_first_simulation_tab(self):
        """Настройка вкладки 'Первая симуляция'."""
        self.create_parameter_entries(self.tabview.tab("Первая симуляция"), self.default_values_first)
        self.create_simulation_button(self.tabview.tab("Первая симуляция"), "Запустить первую симуляцию", self.start_first_simulation)

    def setup_second_simulation_tab(self):
        """Настройка вкладки 'Вторая симуляция'."""
        self.create_parameter_entries(self.tabview.tab("Вторая симуляция"), self.default_values_second)
        self.create_simulation_button(self.tabview.tab("Вторая симуляция"), "Запустить вторую симуляцию", self.start_second_simulation)

    def create_parameter_entries(self, parent, default_values):
        """Создание полей ввода для параметров."""
        self.params_frame = ctk.CTkFrame(parent)
        self.params_frame.pack(padx=10, pady=10, fill="x")

        self.entries = {}
        for param, (value, unit) in default_values.items():
            self.create_parameter_row(param, value, unit)

    def create_parameter_row(self, param, value, unit):
        """Создание строки с полем ввода для одного параметра."""
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

    def create_simulation_button(self, parent, text, command):
        """Создание кнопки запуска симуляции."""
        button = ctk.CTkButton(parent, text=text, command=command)
        button.pack(pady=10)

    def setup_about_tab(self):
        """Настройка вкладки 'О программе'."""
        label = ctk.CTkLabel(self.tabview.tab("О программе"), text="О программе: Моделирование реле")
        label.pack(padx=10, pady=10)

    def start_first_simulation(self):
        """Запуск первой симуляции и отображение результатов."""
        params = {param: float(entry.get()) for param, entry in self.entries.items()}
        self.show_simulation_results(params, run_simulation_first_method)

    def start_second_simulation(self):
        """Запуск второй симуляции и отображение результатов."""
        params = {param: float(entry.get()) for param, entry in self.entries.items()}
        self.show_simulation_results(params, run_simulation_second_method)

    def show_simulation_results(self, params, simulation_function):
        """Отображение результатов симуляции в новом окне."""
        self.graph_window = ctk.CTkToplevel(self.root)
        self.graph_window.title("Результаты симуляции")
        self.graph_window.geometry("100%x100%")  # Увеличим ширину окна для текстового поля
        self.graph_window.resizable(False, False)

        results = simulation_function(params)
        self.plot_results(results)

    def plot_results(self, results):
        """Построение графиков на основе результатов симуляции."""
        plt.style.use('dark_background')
        background_color = '#242424'
        text_color = 'white'
        grid_color = '#555555'

        fig, ax = plt.subplots(figsize=(8, 6))  # Уменьшим размер графика
        fig.suptitle('Результаты симуляции', fontsize=16, color=text_color)
        fig.patch.set_facecolor(background_color)

        ax.plot(results["time"], results["current"], color='#1f77b4')
        ax.set_xlabel('Время (t)', color=text_color)
        ax.set_ylabel('Ток (i)', color=text_color)
        ax.set_title('Зависимость тока от времени', color=text_color)
        ax.grid(True, color=grid_color)
        ax.set_facecolor(background_color)

        plt.tight_layout()

        # Создаем фрейм для графика и текстового поля
        frame = ctk.CTkFrame(self.graph_window)
        frame.pack(fill=ctk.BOTH, expand=True)

        # Добавляем график
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", fill=ctk.BOTH, expand=True, padx=10, pady=10)

        # Анализ тенденций
        trend_analyzer = TrendAnalyzer(results["time"], results["current"])
        trend_info = trend_analyzer.analyze_trends()

        # Добавляем текстовое поле для информации о тенденциях
        text_box = ctk.CTkTextbox(frame, width=400, wrap="word")  # Увеличим ширину текстового поля
        text_box.insert("1.0", trend_info)
        text_box.pack(side="right", fill="both", padx=10, pady=10)

        # Добавляем панель инструментов для графика
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        toolbar_frame = toolbar.winfo_children()[0]
        toolbar_frame.configure(background="#202020")

    def run(self):
        """Запуск главного цикла приложения."""
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()