from  rocket_sim.simulation import simulate_burn, simulate_coast
import pytest
import math

g0 = 9.80665

def test_normal_way():
    result = simulate_burn(300, 1000, 500, 30000, 0.001)
    assert result["time"] == pytest.approx(49.03, abs=0.01)
    assert result["velocity"] == pytest.approx(1558.38, rel=1e-3)
    assert result["height"] == pytest.approx(32476, rel=1e-3)
    
def test_mf():
    result = simulate_burn(300, 1000, 500, 30000)
    assert result["mass"] == pytest.approx(500, rel=1e-3)
    
def test_v():
    g0 = 9.80665
    m0 = 1000
    mf = 500
    thrust = 30000
    
    c = 300 * g0
    t_k = (m0 - mf) / (thrust / c)
    v_k = c * math.log(m0/mf) - g0 * t_k
    
    result1 = simulate_burn(300,1000, 500, 30000, 0.1)
    result2 = simulate_burn(300,1000, 500, 30000, 0.01)
    
    assert abs(result1["velocity"] - v_k) > abs(result2["velocity"] - v_k)

def test_isp_must_be_positive():
    with pytest.raises(ValueError):
        simulate_burn(-2, 1000, 500, 30000)
        
def test_final_mass_zero():
    with pytest.raises(ValueError):
        simulate_burn(300, 1000, 0,30000)
        
def test_isp_zero_raises_error():
    with pytest.raises(ValueError):
        simulate_burn(0,1000,500,30000)

def test_initial_mass_negative():
    with pytest.raises(ValueError):
        simulate_burn(300,-1,500,30000)
        
def test_masses_equal():
    with pytest.raises(ValueError):
        simulate_burn(300,1000,1000,30000)
        
def test_small_thrust():
    with pytest.raises(ValueError):
        simulate_burn(300, 1000, 500, 5000)

def test_dt_zero():
    with pytest.raises(ValueError):
        simulate_burn(300,1000, 500, 30000, 0)
        
def test_dt_negative():
    with pytest.raises(ValueError):
        simulate_burn(300,1000, 500, 30000, -1)
        
def test_mf_more_m0():
    with pytest.raises(ValueError):
        simulate_burn(300, 1000, 2000,30000)

def test_m0_zero():
    with pytest.raises(ValueError):
        simulate_burn(300, 0, 500, 30000)
        
def test_simulate_coast():
    result = simulate_coast(32476, 1558.38, 0.001)
    
    assert result["time"] == pytest.approx(158.9, abs = 0.1)
    assert result["height"] == pytest.approx(156300, rel =1e-3)
    
def test_max_height():
    h0 = 32476
    v0 = 1558.38
    
    h_max = h0 + (v0**2) / (2*g0)
    
    result = simulate_coast(32476, 1558.38, 0.001)
    
    assert result["height"] == pytest.approx(h_max, rel = 1e-3)
    
def test_less_dt():
    g0 = 9.80665
    h0 = 32476
    v0 = 1558.38
    result1 = simulate_coast(32476, 1558.38, 0.01)
    result2 = simulate_coast(32476, 1558.38, 0.0001)
    
    h_max = h0 + (v0**2) / (2*g0)
    
    test1 = abs(result1["height"] - h_max)
    test2 = abs(result2["height"] - h_max)
    
    assert test1 > test2

@pytest.mark.parametrize("h0, v0, dt", [
    (-1, 1558.38, 0.01),    # отрицательная высота
    (32476, 0, 0.01),       # нулевая скорость
    (32476, -5, 0.01),      # отрицательная скорость
    (32476, 1558.38, 0),    # dt = 0
    (32476, 1558.38, -1),   # dt < 0
])

def test_coast_errors(h0,v0,dt):
    with pytest.raises(ValueError):
        simulate_coast(h0,v0,dt)