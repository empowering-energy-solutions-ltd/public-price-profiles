from enum import Enum, auto
### Good source about how to use Enum:: https://codereview.stackexchange.com/questions/267948/using-python-enums-to-define-physical-units


class SimParameters(Enum):
  """Simulation Parameters"""

  COST = 1, "GBP"
  TIMESTEP = 30, "minutes"
  SIMULATION_UNIT = 1, "kW"
  PRICE_UNIT = 1, "GBP/kWh"
  EMISSION_UNIT = 1, "kgCO2e/kWh"

  @property
  def magnitude(self) -> str:
    """Get the magnitude which is most commonly used for this unit."""
    return self.value[0]

  @property
  def units(self) -> str:
    """Get the units for which this unit is relevant."""
    return self.value[1]


class PhysicalQuantity(Enum):
  """List of physical quantities recognized."""

  TEMPERATURE = auto()
  ENERGY = auto()
  TIME = auto()
  MASS = auto()
  LENGTH = auto()
  POWER = auto()
  UNCATEGORIZED = auto()

  @classmethod
  def _missing_(cls, value):
    return cls.UNCATEGORIZED


class EnergyCarrier(Enum):
  """Defines the energy carriers considered"""

  ELECTRICITY = auto()
  NATURALGAS = auto()
  HEATING = auto()
  COOLING = auto()
  UNCATEGORIZED = auto()
  NONE = auto()

  @classmethod
  def _missing_(cls, value):
    return cls.NONE


class Destination(Enum):
  """Defines the possible destinations of the flux"""

  IMPORT = auto()
  EXPORT = auto()
  ONSITE = auto()
  INPUT = auto()
  OUTPUT = auto()
  DEMAND = auto()


class TechnologyType(Enum):
  """Defines the possible destinations of the energy"""

  PV = "Photovoltaics panels"
  WINDTURBINE = "Wind turbine"
  CHPPLANT = "Combined heat and power plant"
  BOILERPLANT = "Boiler"
  UNCATEGORIZED = "Uncategorized"
  HEATPUMP = "Heat-pump"
  GRID = "Main grid"
  SITE = "Site"


class DispatchStrategy(Enum):
  ELECTRICITYLED = auto()
  THERMALLED = auto()
  CUSTOM = auto()
  ACTUAL = auto()


class EnergyCharge(Enum):
  """List of energy charges found on energy invoices."""

  DUOS = auto()
  CCL = auto()
  ENERGY_CHARGE = auto()
  NIGHT_CHARGE = auto()
  DAY_CHARGE = auto()
  DUOS_AMBER = auto()
  DUOS_RED = auto()
  DUOS_GREEN = auto()
  GAS_CHARGE = auto()


class Charts(Enum):
  HH_LABEL = "half-hourly"
  DAILY_LABEL = "daily"
  WEEKLY_LABEL = "weekly"
