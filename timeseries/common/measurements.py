from __future__ import annotations
from dataclasses import dataclass
from typing import Optional

from pint import Unit as pint_unit
from . import ureg


@dataclass
class Unit:
    """Class to deal with physical/economic units"""

    units: pint_unit

    @property
    def dimensionality(self):
        return self.units.dimensionality

    def get_abbreviated_units(self) -> str:
        return f"{self.units:~}".replace(" ", "")

    def convert_to(
        self, new_c_unit: Unit, convert_self: Optional[bool] = True
    ) -> float:
        "Convert the units to the new units and return the conversion factor"
        if isinstance(new_c_unit, str):
            new_c_unit = get_unit(new_c_unit)
        new_quantity = (1 * self.units).to(new_c_unit.units)
        if convert_self:
            self.units = new_quantity.units
        return round(new_quantity.magnitude, 10)


@dataclass
class Quantity:
    """Class to manage quantities and avoid errors when dealing with multiple quantities.
    It uses the pint library to handle the units. It is a wrapper around the pint.Quantity class.
    Args:
        c_unit: Unit 
          The unit of the quantity
        magnitude: float 
          The magnitude of the quantity
          
    Methods:
        dimensionality: str
          Return the dimensionality of the quantity
        units: str
          Return the units of the quantity
        compact: None
          Adjust the quantity for ease of reading. (e.g. GBP*J/kWh->GBP)
        convert_to: float
          Convert the quantity to a new unit and return the magnitude of the new quantity
        __mul__: Quantity
          Multiply the quantity by another quantity or a unit
        __rmul__: Quantity
          Multiply the quantity by another quantity or a unit
          """

    c_unit: Unit
    magnitude: float

    def __post_init__(self):
        self.compact()

    @property
    def dimensionality(self):
        return self.c_unit.dimensionality

    @property
    def units(self):
        return self.c_unit.units

    def get_abbreviated_units(self) -> str:
        return self.c_unit.get_abbreviated_units()

    def compact(self) -> None:
        """Adjust the quantity for ease of reading. (e.g. GBP*J/kWh->GBP)"""
        quantity = (self.magnitude * self.units).to_base_units()
        quantity = (quantity.magnitude * quantity.units).to_compact()
        self.c_unit = Unit(quantity.units)
        self.magnitude = round(quantity.magnitude, 10)

    def convert_to(
        self, new_c_unit: Unit | str, convert_self: Optional[bool] = True
    ) -> float:
        if isinstance(new_c_unit, str):
            new_c_unit = get_unit(new_c_unit)

        new_quantity = (self.magnitude * self.units).to(new_c_unit.units)

        if convert_self:
            self.c_unit = Unit(new_quantity.units)
            self.magnitude = new_quantity.magnitude

        return round(new_quantity.magnitude, 10)

    def __mul__(self, other: Quantity | Unit) -> Quantity:
        if isinstance(other, Unit):
            new_quantity = (self.magnitude * self.units) * (1 * other.units)
        else:
            new_quantity = (self.magnitude * self.units) * (
                other.magnitude * other.units
            )
        new_c_unit = Unit(new_quantity.units)
        return Quantity(new_c_unit, new_quantity.magnitude)

    def __rmul__(self, other: Quantity | Unit) -> Quantity:
        return self.__mul__(other)


def get_unit(unit_name: str) -> Unit:
    """ Create a unit object from the unit name. """
    units: pint_unit = ureg(unit_name).units
    return Unit(units=units)


def get_quantity(unit_name: str, magnitude: float) -> Quantity:
    """ Create a quantity object from the unit name and the magnitude. """
    temp_unit = get_unit(unit_name)
    return Quantity(c_unit=temp_unit, magnitude=magnitude)
