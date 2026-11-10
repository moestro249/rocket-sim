
import math
from dataclasses import dataclass
from physics import drag_force

g0 = 9.80665


@dataclass
class BurnResult:
    time: float
    velocity: float
    height: float
    mass: float


@dataclass
class CoastResult:
    time: float
    height: float


@dataclass
class FlightResult:
    burn_time: float
    burnout_velocity: float
    burnout_height: float
    coast_time: float
    apogee: float
    total_time: float


def simulate_burn(
    isp: float,
    m0: float,
    mf: float,
    thrust: float,
    dt: float = 0.01,
    cd: float = 0.5,
    rho: float = 1.225,
    area: float = 0.01,
) -> BurnResult:

    if not all(math.isfinite(x) for x in (isp, m0, mf, thrust, dt, cd, rho, area)):
        raise ValueError("Все параметры должны быть конечными числами")

    if isp <= 0 or m0 <= 0 or mf <= 0:
        raise ValueError("Импульс и массы должны быть положительными")

    if m0 <= mf:
        raise ValueError("Начальная масса должна быть больше конечной")

    if thrust <= m0 * g0:
        raise ValueError("Тяга должна превышать начальный вес ракеты")

    if dt <= 0:
        raise ValueError("Шаг интегрирования должен быть положительным")

    if cd < 0 or rho < 0 or area <= 0:
        raise ValueError("Недопустимые аэродинамические параметры")

    m = m0
    c = isp * g0
    mdot = thrust / c
    t_k = (m0 - mf) / mdot

    v = 0.0
    h = 0.0
    t = 0.0

    while t < t_k:
        step = min(dt, t_k - t)

        f_d = drag_force(v, cd, rho, area)
        a = (thrust + f_d) / m - g0

        h += v * step + 0.5 * a * step**2
        v += a * step
        m -= mdot * step
        t += step

    return BurnResult(
        time=t,
        velocity=v,
        height=h,
        mass=m
    )


def simulate_coast(
    h0: float,
    v0: float,
    dt: float = 0.01,
    *,
    mass: float | None = None,
    cd: float = 0.5,
    rho: float = 1.225,
    area: float = 0.01,
) -> CoastResult:

    if not all(math.isfinite(x) for x in (h0, v0, dt, cd, rho, area)):
        raise ValueError("Все параметры должны быть конечными числами")

    if h0 < 0 or v0 <= 0:
        raise ValueError("Высота должна быть неотрицательной, скорость положительной")

    if dt <= 0:
        raise ValueError("Шаг интегрирования должен быть положительным")

    if mass is not None and (not math.isfinite(mass) or mass <= 0):
        raise ValueError("Масса должна быть положительной")

    if cd < 0 or rho < 0 or area <= 0:
        raise ValueError("Недопустимые аэродинамические параметры")

    h = h0
    v = v0
    t = 0.0

    while v > 0:
        step = min(dt, v / g0)

        f_d = drag_force(v, cd, rho, area)
        a = f_d / mass - g0

        h += v * step + 0.5 * a * step**2
        v += a * step
        t += step

    return CoastResult(time=t, height=h)


def simulate_flight(
    isp: float,
    m0: float,
    mf: float,
    thrust: float,
    dt: float = 0.01,
    cd: float = 0.5,
    rho: float = 1.225,
    area: float = 0.01,
) -> FlightResult:

    burn = simulate_burn(
        isp, m0, mf, thrust, dt, cd, rho, area
    )

    coast = simulate_coast(
        burn.height,
        burn.velocity,
        dt,
        mass=mf,
        cd=cd,
        rho=rho,
        area=area
    )

    return FlightResult(
        burn_time=burn.time,
        burnout_velocity=burn.velocity,
        burnout_height=burn.height,
        coast_time=coast.time,
        apogee=coast.height,
        total_time=burn.time + coast.time
    )


def format_flight_result(result: FlightResult) -> str:
    return (
        f"Flight results:\n"
        f"Burn time: {result.burn_time:.2f} s\n"
        f"Burnout velocity: {result.burnout_velocity:.2f} m/s\n"
        f"Apogee: {result.apogee:.2f} m\n"
        f"Total time to apogee: {result.total_time:.2f} s"
    )
