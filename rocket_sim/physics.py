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
    
def drag_force(v: float, cd: float, rho: float, area: float) -> float:
    if not all(math.isfinite(x) for x in (v, cd, rho, area)):
        raise ValueError("Все параметры должны быть конечными числами")
    if cd < 0:
        raise ValueError("Коэффициент сопротивления не может быть отрицательным")

    if rho < 0:
        raise ValueError("Плотность воздуха не может быть отрицательной")

    if area <= 0:
        raise ValueError("Площадь поперечного сечения должна быть больше нуля")
    f_d = - ((cd * rho * area) * (v * abs(v)))/2
    
    return f_d