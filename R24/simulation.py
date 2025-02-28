import math
import numpy as np

class ElectromagneticSystem:
    def __init__(self):
        pass

    def calculate_first_method(self, U, R, L0, δ0, δk, Fнач, M, μ0, W, S, m, dt):
        t = 0.0
        tmax = 0.3
        δ = δ0
        L = L0 / δ0
        s0 = (Fнач / M) + δ0
        E = (μ0 * (W**2) * S) / 2

        time = []
        current = []

        while t < tmax:
            try:
                τ = L / R
                i = (U / R) * (1 - math.exp(-t / τ))

                Fэ = E * ((i / δ) ** 2)
                Fм = M * (s0 - δ)
                F_result = Fм - Fэ

                if δ >= δ0 and F_result > 0:
                    F_result = 0
                elif δ <= δk and F_result < 0:
                    F_result = 0

                a_result = F_result / m

                δ += (a_result * (dt**2)) / 2
                L = L0 / δ

                time.append(t)
                current.append(i)

                t += dt

            except OverflowError:
                continue

        return {
            "time": time,
            "current": current,
        }

    def calculate_second_method(self, U, R, L0, δ0, δk, Fнач, M, μ0, W, S, m, dt, R1, C, ΔU):
        t = 0.0
        tmax = 0.3
        δ = δ0
        L = L0 / δ0
        s0 = (Fнач / M) + δ0
        E = (μ0 * (W**2) * S) / 2

        time = []
        current = []

        Uвх = U + ΔU

        while t < tmax:
            try:
                a = R1 * C * L
                b = L + R * R1 * C
                Δ = b**2 - 4 * a * (R + R1)
                p1 = (-b + math.sqrt(Δ)) / (2 * a)
                p2 = (-b - math.sqrt(Δ)) / (2 * a)

                A1 = (Uвх * R1 * C * p1 + Uвх) / (3 * R1 * C * L * p1**2 + 2 * (L + R * R1 * C) * p1 + R + R1)
                A2 = (Uвх * R1 * C * p2 + Uвх) / (3 * R1 * C * L * p2**2 + 2 * (L + R * R1 * C) * p2 + R + R1)

                i_prog = Uвх / (R + R1)
                i_sv = A1 * math.exp(p1 * t) + A2 * math.exp(p2 * t)
                i = i_prog + i_sv

                Fэ = E * ((i / δ) ** 2)
                Fм = M * (s0 - δ)
                F = Fм - Fэ

                if δ >= δ0 and F > 0:
                    F = 0
                elif δ <= δk and F < 0:
                    F = 0

                a = F / m
                δ += (a * (dt**2)) / 2
                L = L0 / δ

                t += dt
                time.append(t)
                current.append(i)

            except OverflowError:
                break

        return {
            "time": time,
            "current": current,
        }

def run_simulation_first_method(params):
    μ0 = 4 * math.pi * 10**-7
    S = (math.pi * (params["D"]**2)) / 4
    L0 = (params["W"]**2) * μ0 * S

    system = ElectromagneticSystem()

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

def run_simulation_second_method(params):
    μ0 = 4 * math.pi * 10**-7
    S = (math.pi * (params["D"]**2)) / 4
    L0 = (params["W"]**2) * μ0 * S

    system = ElectromagneticSystem()

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

        for i in range(1, len(self.current_diff)):
            if self.current_diff[i] > 0 and self.current_diff[i-1] <= 0:
                events.append((self.time[i], "рост", self.current[i]))
            elif self.current_diff[i] < 0 and self.current_diff[i-1] >= 0:
                events.append((self.time[i], "падение", self.current[i]))

        if not events:
            trend_info += "Нет значительных изменений тенденции.\n"
            return trend_info

        first_event_time = events[0][0]
        trend_info += f"Время перед первым изменением: {first_event_time:.6f} с\n\n"

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