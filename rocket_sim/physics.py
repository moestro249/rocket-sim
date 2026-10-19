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
        delta_v = isp * g0 * math.log(m0/mf)
        return delta_v
