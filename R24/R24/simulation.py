import math

class ElectromagneticSystem:
    def __init__(self, U, R, L0, δ0, δk, Fнач, M, μ0, W, S, m, dt):
        # Инициализация параметров системы
        self.U = U  # Напряжение
        self.R = R  # Сопротивление
        self.L0 = L0  # Начальная индуктивность
        self.δ0 = δ0  # Начальное значение δ
        self.δk = δk  # Конечное значение δ
        self.Fнач = Fнач  # Начальная сила
        self.M = M  # Масса
        self.μ0 = μ0  # Магнитная проницаемость
        self.W = W  # Количество витков
        self.S = S  # Площадь сечения
        self.m = m  # Масса
        self.dt = dt  # Шаг времени

        # Инициализация переменных
        self.t = 0.0  # Начальное время
        self.tmax = 0.3  # Максимальное время
        self.δ = δ0  # Текущее значение δ
        self.L = L0 / δ0  # Текущая индуктивность
        self.s0 = (Fнач / M) + δ0  # Начальное смещение
        self.E = (μ0 * (W**2) * S) / 2  # Энергия

        # Списки для хранения данных
        self.time = []  # Время
        self.current = []  # Ток
        self.tau = []  # Время τ
        self.Fe = []  # Сила Fэ
        self.Fm = []  # Сила Fм
        self.F = []  # Результирующая сила F
        self.a = []  # Ускорение a
        self.delta = []  # Текущее значение δ
        self.inductance = []  # Текущая индуктивность L

    def calculate(self):
        while self.t < self.tmax:
            try:
                # Расчет времени τ и тока i
                τ = self.L / self.R
                i = (self.U / self.R) * (1 - math.exp(-self.t / τ))

                # Расчет сил Fэ и Fм
                Fэ = self.E * ((i / self.δ) ** 2)
                Fм = self.M * (self.s0 - self.δ)

                # Результирующая сила
                F = Fм - Fэ

                # Условия для ограничения силы F
                if self.δ >= self.δ0 and F > 0:
                    F = 0
                elif self.δ <= self.δk and F < 0:
                    F = 0

                # Ускорение
                a = F / self.m

                # Обновление δ и L
                self.δ += (a * (self.dt**2)) / 2
                self.L = self.L0 / self.δ

                # Сохранение данных
                self.time.append(self.t)
                self.current.append(i)
                self.tau.append(τ)
                self.Fe.append(Fэ)
                self.Fm.append(Fм)
                self.F.append(F)
                self.a.append(a)
                self.delta.append(self.δ)
                self.inductance.append(self.L)

                # Обновление времени
                self.t += self.dt

            except OverflowError:
                # В случае переполнения прерываем цикл
                continue

        # Возвращаем результаты в виде словаря
        return {
            "time": self.time,
            "current": self.current,
            "tau": self.tau,
            "Fe": self.Fe,
            "Fm": self.Fm,
            "F": self.F,
            "a": self.a,
            "delta": self.delta,
            "inductance": self.inductance,
        }

# Функция для запуска симуляции с параметрами
def run_simulation(params):
    # Расчет L0 и S
    μ0 = 4 * math.pi * 10**-7
    S = (math.pi * (params["D"]**2)) / 4
    L0 = (params["W"]**2) * μ0 * S

    # Создание объекта системы
    system = ElectromagneticSystem(
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

    # Запуск расчетов и возврат результатов
    return system.calculate()