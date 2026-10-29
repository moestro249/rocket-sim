import math

g0 = 9.80665

def tsiolkovsky_delta_v(isp: float, m0: float, mf: float) -> float:
    if m0 <= 0:
        raise ValueError("начальная масса должна быть больше нуля")
    elif mf <= 0:
        raise ValueError("Конечная масса должна быть больше нуля")
    elif m0 <= mf or math.isclose(m0,mf):
        raise ValueError("начальная масса должна быть больше конечной")
    elif isp <= 0:
        raise ValueError("Удельный импульс должен быть больше нуля")
    else:
        dv = isp * g0 * math.log(m0/mf)
        return dv

def simulate_coast(h0: float, v0: float, dt: float = 0.01) -> dict:
    if h0 < 0:
        raise ValueError("начальная высота должна быть не меньше нуля")
    elif v0 < 0:
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