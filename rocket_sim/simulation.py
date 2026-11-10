
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

    params = (isp, m0, mf, thrust, dt, cd, rho, area)

    if not all(math.isfinite(x) for x in params):
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

    c = isp * g0
    mdot = thrust / c
    burn_time = (m0 - mf) / mdot

    m = m0
    v = 0.0
    h = 0.0
    t = 0.0

    while t < burn_time:
        step = min(dt, burn_time - t)

        f_d = drag_force(v, cd, rho, area)
        a = (thrust + f_d) / m - g0

        h += v * step + 0.5 * a * step**2
        v += a * step
        m -= mdot * step
        t += step

    m = mf

    return BurnResult(
        time=burn_time,
        velocity=v,
        height=h,
        mass=m,
    )


def simulate_coast(
    h0: float,
    v0: float,
    mass: float,
    dt: float = 0.01,
    cd: float = 0.5,
    rho: float = 1.225,
    area: float = 0.01,
) -> CoastResult:

    params = (h0, v0, mass, dt, cd, rho, area)

    if not all(math.isfinite(x) for x in params):
        raise ValueError("Все параметры должны быть конечными числами")

    if h0 < 0:
        raise ValueError("Начальная высота должна быть неотрицательной")

    if v0 <= 0:
        raise ValueError("Начальная скорость должна быть положительной")

    if mass <= 0:
        raise ValueError("Масса должна быть положительной")

    if dt <= 0:
        raise ValueError("Шаг интегрирования должен быть положительным")

    if cd < 0 or rho < 0 or area <= 0:
        raise ValueError("Недопустимые аэродинамические параметры")

    h = h0
    v = v0
    t = 0.0

    while v > 0:
        f_d = drag_force(v, cd, rho, area)
        a = f_d / mass - g0

        # Шаг ограничивается моментом достижения нулевой скорости
        step = min(dt, -v / a)

        h += v * step + 0.5 * a * step**2
        v += a * step
        t += step

    return CoastResult(
        time=t,
        height=h,
    )


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
        isp=isp,
        m0=m0,
        mf=mf,
        thrust=thrust,
        dt=dt,
        cd=cd,
        rho=rho,
        area=area,
    )

    coast = simulate_coast(
        h0=burn.height,
        v0=burn.velocity,
        mass=burn.mass,
        dt=dt,
        cd=cd,
        rho=rho,
        area=area,
    )

    return FlightResult(
        burn_time=burn.time,
        burnout_velocity=burn.velocity,
        burnout_height=burn.height,
        coast_time=coast.time,
        apogee=coast.height,
        total_time=burn.time + coast.time,
    )


def format_flight_result(result: FlightResult) -> str:
    return (
        f"Flight results:\n"
        f"Burn time: {result.burn_time:.2f} s\n"
        f"Burnout velocity: {result.burnout_velocity:.2f} m/s\n"
        f"Apogee: {result.apogee:.2f} m\n"
        f"Total time to apogee: {result.total_time:.2f} s"
    )
