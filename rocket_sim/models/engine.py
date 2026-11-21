from dataclasses import dataclass
import math

g0 = 9.80665


@dataclass
class Engine:
    thrust: float
    isp: float
    burn_time: float
    fuel_mass: float
    
    def __post_init__(self):
        params =  (
            self.thrust,
            self.isp,
            self.burn_time,
            self.fuel_mass
        )
        
        if not all(math.isfinite(x) for x in params):
            raise ValueError("All engine parameters must be finite numbers")
        
        if self.thrust <= 0:
            raise ValueError("Thrust must be positive")
        
        if self.isp <= 0:
            raise ValueError("Specific impulse must be positive")
        
        if self.burn_time <= 0:
            raise ValueError("Burn time must be positive")
        
        if self.fuel_mass <= 0:
            raise ValueError("Fuel mass must be positive")
        
    @property
    def mass_flow_rate(self) -> float:
        return self.thrust / (self.isp * g0)
    
    @property
    def total_impulse(self) -> float:
        return self.thrust * self.burn_time
    
    @property
    def calculated_fuel_mass(self) -> float:
        return self.mass_flow_rate * self.burn_time
    