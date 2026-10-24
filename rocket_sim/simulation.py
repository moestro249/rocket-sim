import math

g0 = 9.80665

def simulation(isp: float, m0: float, mf: float, thrust: float, dt = 0.01) -> float:
    t = 0
    h = 0
    v = 0
    m = m0
    
    c = isp * g0
    mdot = thrust / c
    
    while mf<=m:
        a = thrust / m - g0
        h += v * dt
        v += a * dt
        m -= mdot * dt
        t += dt
    
    return v