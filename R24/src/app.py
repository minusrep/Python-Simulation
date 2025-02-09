import customtkinter as ctk
from customtkinter import CTkTabview
from simulation import run_simulation
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class App:
    def __init__(self):
        self.setup_ui()
        self.setup_tabs()
        self.setup_default_values()
        self.setup_simulation_tab()
        self.setup_settings_tab()
        self.setup_about_tab()

    def setup_ui(self):
        """Настройка основного интерфейса приложения."""
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Моделирование реле")
        self.root.geometry("10%40%")
        self.root.resizable(False, False)

    def setup_tabs(self):
        """Создание вкладок."""
        self.tabview = CTkTabview(self.root)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        self.tabview.add("Симуляция")
        self.tabview.add("Настройки")
        self.tabview.add("О программе")

    def setup_default_values(self):
        """Установка значений по умолчанию для параметров."""
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

    def setup_simulation_tab(self):
        """Настройка вкладки 'Симуляция'."""
        self.create_parameter_entries(self.tabview.tab("Симуляция"))
        self.create_plot_selection(self.tabview.tab("Симуляция"))
        self.create_simulation_button(self.tabview.tab("Симуляция"))

    def create_parameter_entries(self, parent):
        """Создание полей ввода для параметров."""
        self.params_frame = ctk.CTkFrame(parent)
        self.params_frame.pack(padx=10, pady=10, fill="x")

        self.entries = {}
        for param, (value, unit) in self.default_values.items():
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

    def create_plot_selection(self, parent):
        """Создание раскрывающегося фрейма для выбора графиков."""
        self.plot_selection_frame = ctk.CTkFrame(parent)
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

        self.plot_selection_inner_frame.pack_forget()

    def create_simulation_button(self, parent):
        """Создание кнопки запуска симуляции."""
        self.button = ctk.CTkButton(parent, text="Запустить симуляцию", command=self.start_simulation)
        self.button.pack(pady=10)

    def setup_settings_tab(self):
        """Настройка вкладки 'Настройки'."""
        label = ctk.CTkLabel(self.tabview.tab("Настройки"), text="Здесь будут настройки")
        label.pack(padx=10, pady=10)

    def setup_about_tab(self):
        """Настройка вкладки 'О программе'."""
        label = ctk.CTkLabel(self.tabview.tab("О программе"), text="О программе: Моделирование реле")
        label.pack(padx=10, pady=10)

    def toggle_plot_selection(self):
        """Переключение видимости фрейма с выбором графиков."""
        if self.plot_selection_visible:
            self.plot_selection_inner_frame.pack_forget()
            self.plot_selection_visible = False
        else:
            self.plot_selection_inner_frame.pack(fill="x", padx=5, pady=5)
            self.plot_selection_visible = True

    def start_simulation(self):
        """Запуск симуляции и отображение результатов."""
        params = {param: float(entry.get()) for param, entry in self.entries.items()}
        self.show_simulation_results(params)

    def show_simulation_results(self, params):
        """Отображение результатов симуляции в новом окне."""
        self.graph_window = ctk.CTkToplevel(self.root)
        self.graph_window.title("Результаты симуляции")
        self.graph_window.geometry("800x600")

        results = run_simulation(params)
        self.plot_results(results)

    def plot_results(self, results):
        """Построение графиков на основе результатов симуляции."""
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

        if num_plots == 1:
            axes = [axes]
        elif rows == 1:
            axes = axes.reshape(1, -1)

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
            ax = axes[i // cols][i % cols] if num_plots > 1 else axes[i]
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

        toolbar = NavigationToolbar2Tk(canvas, self.graph_window)
        toolbar.update()
        toolbar_frame = toolbar.winfo_children()[0]
        toolbar_frame.configure(background="#202020")

    def run(self):
        """Запуск главного цикла приложения."""
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()