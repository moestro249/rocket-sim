import math
from dataclasses import dataclass

g0 = 9.80665
#isp - удельный импульс
# c - скорость истечения газов
# thrust - тяга двигателя
# mdot - сек массовый расход двигателя

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
    
def simulate_burn(isp: float, m0: float, mf: float, thrust: float, dt: float = 0.01) -> BurnResult:
    
    if m0 <= 0:
        raise ValueError("начальная масса должна быть больше нуля")
    elif mf <= 0:
        raise ValueError("Конечная масса должна быть больше нуля")
    elif m0 <= mf or math.isclose(m0,mf):
        raise ValueError("начальная масса должна быть больше конечной")
    elif isp <= 0:
        raise ValueError("Удельный импульс должен быть больше нуля")
    elif thrust <= m0 * g0:
        raise ValueError("тяга двигателя должна быть больше вес ракеты")
    elif dt <=0:
        raise ValueError("изменение времени > 0")
    m = m0
    c = isp * g0
    mdot = thrust / c
    t_k = (m0 - mf) / mdot
    
    v = 0
    h = 0
    t = 0
    
    while t < t_k:
        step = min(dt, t_k - t)
        a = thrust / m - g0
        h += v * step - (g0 * step**2)/2
        v += a * step
        m -= mdot * step
        t += step
        
    return BurnResult(
            time = t,
            velocity = v,
            height = h,
            mass = m
        )
    
def simulate_coast(h0: float, v0: float, dt: float = 0.01) -> CoastResult:
    if h0 < 0:
        raise ValueError("начальная высота должна быть не меньше нуля")
    elif v0 <= 0:
        raise ValueError("Начальная скорость должна быть больше нуля")
    elif dt <= 0:
        raise ValueError("Изменение времени должно быть больше нуля")
    
    h = h0
    v = v0
    t = 0
    step = dt
    
    while v > 0:
        t_rem = v/g0
        a = -g0
        h += v * step - (g0 * step**2)/2
        v += a * step
        t += step
        step = min(dt, t_rem)
    return CoastResult(
        time=t,
        height=h
    )

def simulate_flight(isp: float, m0: float, mf: float, thrust: float, dt: float = 0.01) -> FlightResult:
    result1 = simulate_burn(isp, m0,mf, thrust,dt)
    result2 = simulate_coast(result1.height, result1.velocity,dt)
    
    return FlightResult(
        burn_time = result1.time,
        burnout_velocity = result1.velocity,
        burnout_height = result1.height,
        coast_time = result2.time,
        apogee = result2.height,
        total_time = result1.time + result2.time
    )
    