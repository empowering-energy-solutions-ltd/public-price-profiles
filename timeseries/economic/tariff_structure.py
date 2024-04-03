from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd
from timeseries.common import enums, measurements


@dataclass
class ConsumptionCharges:
  """Object to represent the consumption charges £/kWh.
    The charges can be dependent on time (half-hour, day of week, etc.)"""

  energy_charge_name: str
  series: pd.Series

  def __post_init__(self):
    print(f"post_init of {self.energy_charge_name}")

  @property
  def name(self):
    return self.energy_charge_name

  def get_charges_by_datetime(self, date_time: datetime) -> float:
    return self.series.loc[date_time]


@dataclass
class TariffStructure:
  """Create an energy tariff structure."""
  energy_carrier: enums.EnergyCarrier
  destination: enums.Destination
  origin: enums.TechnologyType
  units: measurements.Unit | None = None
  list_consumption_charges: list[ConsumptionCharges] = field(
      default_factory=list)

  def __post_init__(self):
    print("post init")
    if self.units is None:
      self.units = measurements.get_unit(
          unit_name=enums.SimParameters.PRICE_UNIT.units)

  @property
  def name(self) -> str:
    return f"{self.energy_carrier.name}_{self.destination.name}"

  def get_consumption_charges_dataframe(self) -> pd.DataFrame:
    list_values = []
    dates = []
    names = []
    assert self.list_consumption_charges is not None
    for temp_charges in self.list_consumption_charges:
      list_values.append(temp_charges.series.values)
      dates = temp_charges.series.index
      names.append(temp_charges.name)
    return pd.DataFrame(index=names, columns=dates, data=list_values).T

  def get_total_consumption_charges(self, date_time: datetime) -> float:
    cost = 0
    assert self.list_consumption_charges is not None
    for temp_charges in self.list_consumption_charges:
      cost += temp_charges.get_charges_by_datetime(date_time)

    return cost

  def add_component(self):
    pass

  def remove_component(self):
    pass
