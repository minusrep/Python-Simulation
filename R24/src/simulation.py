import math

class ElectromagneticSystem:
    def __init__(self):
        # Инициализация переменных (если они нужны для общего использования)
        pass

    def calculate(self, U, R, L0, δ0, δk, Fнач, M, μ0, W, S, m, dt):
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

# Функция для запуска симуляции с параметрами
def run_simulation(params):
    # Расчет L0 и S
    μ0 = 4 * math.pi * 10**-7
    S = (math.pi * (params["D"]**2)) / 4
    L0 = (params["W"]**2) * μ0 * S

    # Создание объекта системы
    system = ElectromagneticSystem()

    # Запуск расчетов и возврат результатов
    return system.calculate(
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