import math
import numpy as np

class ElectromagneticSystem:
    def __init__(self):
        # Инициализация переменных (если они нужны для общего использования)
        pass

    def calculate_first_method(self, U, R, L0, δ0, δk, Fнач, M, μ0, W, S, m, dt):
        # Инициализация переменных для текущего расчета
        t = 0.0  # Начальное время
        tmax = 0.3  # Максимальное время
        δ = δ0  # Текущее значение δ
        L = L0 / δ0  # Текущая индуктивность
        s0 = (Fнач / M) + δ0  # Начальное смещение
        E = (μ0 * (W**2) * S) / 2  # Энергия

        # Списки для хранения данных
        time = []  # Время
        current = []  # Ток
        tau = []  # Время τ
        Fe = []  # Сила Fэ
        Fm = []  # Сила Fм
        F = []  # Результирующая сила F
        a = []  # Ускорение a
        delta = []  # Текущее значение δ
        inductance = []  # Текущая индуктивность L

        while t < tmax:
            try:
                # Расчет времени τ и тока i
                τ = L / R
                i = (U / R) * (1 - math.exp(-t / τ))

                # Расчет сил Fэ и Fм
                Fэ = E * ((i / δ) ** 2)
                Fм = M * (s0 - δ)

                # Результирующая сила
                F_result = Fм - Fэ

                # Условия для ограничения силы F
                if δ >= δ0 and F_result > 0:
                    F_result = 0
                elif δ <= δk and F_result < 0:
                    F_result = 0

                # Ускорение
                a_result = F_result / m

                # Обновление δ и L
                δ += (a_result * (dt**2)) / 2
                L = L0 / δ

                # Сохранение данных
                time.append(t)
                current.append(i)
                tau.append(τ)
                Fe.append(Fэ)
                Fm.append(Fм)
                F.append(F_result)
                a.append(a_result)
                delta.append(δ)
                inductance.append(L)

                # Обновление времени
                t += dt

            except OverflowError:
                # В случае переполнения прерываем цикл
                continue

        # Возвращаем результаты в виде словаря
        return {
            "time": time,
            "current": current,
            "tau": tau,
            "Fe": Fe,
            "Fm": Fm,
            "F": F,
            "a": a,
            "delta": delta,
            "inductance": inductance,
        }

    def calculate_second_method(self, U, R, L0, δ0, δk, Fнач, M, μ0, W, S, m, dt, R1, C, ΔU):
        # Инициализация переменных для текущего расчета
        t = 0.0  # Начальное время
        tmax = 0.3  # Максимальное время
        δ = δ0  # Текущее значение δ
        L = L0 / δ0  # Текущая индуктивность
        s0 = (Fнач / M) + δ0  # Начальное смещение
        E = (μ0 * (W**2) * S) / 2  # Энергия

        # Списки для хранения данных
        time = []  # Время
        current = []  # Ток

        Uвх = U + ΔU  # Входное напряжение с учетом ΔU

        while t < tmax:
            try:
                # Расчет корней характеристического уравнения
                a = R1 * C * L
                b = L + R * R1 * C
                Δ = b**2 - 4 * a * (R + R1)
                p1 = (-b + math.sqrt(Δ)) / (2 * a)
                p2 = (-b - math.sqrt(Δ)) / (2 * a)

                # Расчет коэффициентов A1 и A2
                A1 = (Uвх * R1 * C * p1 + Uвх) / (3 * R1 * C * L * p1**2 + 2 * (L + R * R1 * C) * p1 + R + R1)
                A2 = (Uвх * R1 * C * p2 + Uвх) / (3 * R1 * C * L * p2**2 + 2 * (L + R * R1 * C) * p2 + R + R1)

                # Расчет тока i(t)
                i_prog = Uвх / (R + R1)  # Установившаяся составляющая
                i_sv = A1 * math.exp(p1 * t) + A2 * math.exp(p2 * t)  # Свободная составляющая
                i = i_prog + i_sv

                # Расчет сил
                Fэ = E * ((i / δ) ** 2)
                Fм = M * (s0 - δ)
                F = Fм - Fэ

                # Проверка условий для силы F
                if δ >= δ0 and F > 0:
                    F = 0
                elif δ <= δk and F < 0:
                    F = 0

                # Расчет ускорения и обновление зазора
                a = F / m
                δ += (a * (dt**2)) / 2
                L = L0 / δ

                # Обновление времени и сохранение данных
                t += dt
                time.append(t)
                current.append(i)

            except OverflowError:
                break

        # Возвращаем результаты в виде словаря
        return {
            "time": time,
            "current": current,
        }

# Функция для запуска первой симуляции
def run_simulation_first_method(params):
    # Расчет L0 и S
    μ0 = 4 * math.pi * 10**-7
    S = (math.pi * (params["D"]**2)) / 4
    L0 = (params["W"]**2) * μ0 * S

    # Создание объекта системы
    system = ElectromagneticSystem()

    # Запуск расчетов и возврат результатов
    return system.calculate_first_method(
        U=params["U"],
        R=params["R"],
        L0=L0,
        δ0=params["δ0"],
        δk=params["δk"],
        Fнач=params["Fнач"],
        M=params["M"],
        μ0=μ0,
        W=params["W"],
        S=S,
        m=params["m"],
        dt=params["dt"],
    )

# Функция для запуска второй симуляции
def run_simulation_second_method(params):
    # Расчет L0 и S
    μ0 = 4 * math.pi * 10**-7
    S = (math.pi * (params["D"]**2)) / 4
    L0 = (params["W"]**2) * μ0 * S

    # Создание объекта системы
    system = ElectromagneticSystem()

    # Запуск расчетов и возврат результатов
    return system.calculate_second_method(
        U=params["U"],
        R=params["R"],
        L0=L0,
        δ0=params["δ0"],
        δk=params["δk"],
        Fнач=params["Fнач"],
        M=params["M"],
        μ0=μ0,
        W=params["W"],
        S=S,
        m=params["m"],
        dt=params["dt"],
        R1=params["R1"],
        C=params["C"],
        ΔU=params["ΔU"],
    )

class TrendAnalyzer:
    def __init__(self, time, current):
        self.time = time
        self.current = current
        self.current_diff = np.diff(current)
        self.time_diff = np.diff(time)

    def analyze_trends(self):
        """Анализ тенденций изменения графика."""
        trend_info = "Информация о тенденциях:\n\n"
        events = []

        # Поиск точек изменения тенденции
        for i in range(1, len(self.current_diff)):
            if self.current_diff[i] > 0 and self.current_diff[i-1] <= 0:
                events.append((self.time[i], "рост", self.current[i]))
            elif self.current_diff[i] < 0 and self.current_diff[i-1] >= 0:
                events.append((self.time[i], "падение", self.current[i]))

        if not events:
            trend_info += "Нет значительных изменений тенденции.\n"
            return trend_info

        # Время перед первым изменением
        first_event_time = events[0][0]
        trend_info += f"Время перед первым изменением: {first_event_time:.6f} с\n\n"

        # Анализ каждого события
        for i, (event_time, event_type, event_value) in enumerate(events):
            trend_info += f"Событие {i+1}:\n"
            trend_info += f"  Время: {event_time:.6f} с\n"
            trend_info += f"  Тип: {event_type}\n"
            trend_info += f"  Значение y: {event_value:.6f}\n"

            if i > 0:
                prev_event_time = events[i-1][0]
                time_interval = event_time - prev_event_time
                trend_info += f"  Промежуток времени с предыдущим событием: {time_interval:.6f} с\n"

            trend_info += "\n"

        return trend_info