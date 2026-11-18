import math
from dataclasses import dataclass
@dataclass
class Rocket:
    dry_mass: float
    fuel_mass: float
    diameter: float
    drag_coefficient: float
    
    def __post_init__(self):
    # Проверяем, что все параметры являются конечными числами
        if not all(math.isfinite(x) for x in (
            self.dry_mass,
            self.fuel_mass,
            self.diameter,
            self.drag_coefficient
        )):
            raise ValueError("All parameters must be finite numbers")
    
    # Проверяем сухую массу
        if self.dry_mass <= 0:
            raise ValueError("Dry mass must be positive")
    
    # Проверяем массу топлива
        if self.fuel_mass < 0:
            raise ValueError("Fuel mass cannot be negative")
    
    # Проверяем массу топлива
        if self.fuel_mass < 0:
            raise ValueError("Fuel mass cannot be negative")
    
    # Проверяем диаметр
        if self.diameter <= 0:
            raise ValueError("Diameter must be positive")

    # Проверяем коэффициент сопротивления
        if self.drag_coefficient < 0:
            raise ValueError("Drag coefficient cannot be negative")
    
    @property
    def total_mass(self):
        total_mass = self.dry_mass + self.fuel_mass
        return total_mass

    @property
    def cross_section_area(self):
        s = math.pi * self.diameter**2 / 4
        return s

rocket = Rocket(500, 1500, 1.2, 0.4)

print(rocket.total_mass)
print(rocket.cross_section_area)
    