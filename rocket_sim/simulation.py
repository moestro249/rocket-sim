import math

g0 = 9.80665
#isp - удельный импульс
# c - скорость истечения газов
# thrust - тяга двигателя
# mdot - сек массовый расход двигателя

def simulate_burn(isp: float, m0: float, mf: float, thrust: float, dt: float = 0.01) -> dict:
    
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
        raise ValueError("изменение времени >0")
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
        h += v * step
        v += a * step
        m -= mdot * step
        t += step

    return {
        "time": t,
        "velocity": v,
        "height": h,
        "mass": m
    }
    
def simulate_coast(h0: float, v0: float, dt: float = 0.01) -> dict:
    if h0 < 0:
        raise ValueError("начальная высота должна быть не меньше нуля")
    elif v0 <= 0:
        raise ValueError("Начальная скорость должна быть не меньше нуля")
    elif dt <= 0:
        raise ValueError("Изменение времени должно быть больше нуля")
    
    h = h0
    v = v0
    t = 0
    
    while v > 0:
        a = -g0
        h += v * dt
        v += a * dt
        t += dt
    else:
        result = {
            "time": t,
            "height": h
        }
        return result