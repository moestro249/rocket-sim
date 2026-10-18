from rocket_sim.physics import tsiolkovsky_delta_v
import pytest

def test_delta_v_normal(): 
    result = tsiolkovsky_delta_v(300, 1000, 500)
    
    assert result == pytest.approx(2039.2, abs=0.1)
    
def test_isp_must_be_positive():
    with pytest.raises(ValueError):
        tsiolkovsky_delta_v(-2, 1000, 500)
        
def test_final_mass_zero():
    with pytest.raises(ValueError):
        tsiolkovsky_delta_v(300, 1000, 0)
        
def test_isp_zero_raises_error():
    with pytest.raises(ValueError):
        tsiolkovsky_delta_v(0,1000,500)

def test_initial_mass_negative():
    with pytest.raises(ValueError):
        tsiolkovsky_delta_v(300,-1,500)
        
def test_masses_equal():
    with pytest.raises(ValueError):
        tsiolkovsky_delta_v(300,1000,1000)

def test_final_mass_greater_than_initial():
    with pytest.raises(ValueError):
        tsiolkovsky_delta_v(300,500,1000)

def test_masses_almost_equal():
    result1 = tsiolkovsky_delta_v(300, 1000, 499.999)
    result2 = tsiolkovsky_delta_v(300, 1000, 500)
    
    assert result2 < result1
    
        