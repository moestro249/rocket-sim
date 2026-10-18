import math

g0 = 9.80665

def tsiolkovsky_delta_v(isp: float, m0: float, mf: float) -> float:
    if m0 <= 0:
        raise ValueError("начальная масса должна быть больше нуля")
    elif mf <= 0:
        raise ValueError("Конечная масса должна быть больше нуля")
    elif abs(m0, 0.1) <= abs(mf, 0.1):
        raise ValueError("начальная масса должна быть больше конечной")
    elif isp <= 0:
        raise ValueError("Удельный импульс должен быть больше нуля")
    else:
        delta_v = isp * g0 * math.log(m0/mf)
        return delta_v
    
    
print(tsiolkovsky_delta_v())

