from dataclasses import dataclass
from timeseries.common import enums


@dataclass
class BaseImportElectricityPriceSchema:
  """Schema for import electricity price data."""
  consumption_day_charges = ([
      "Consumption_charges", "Consumption_day_charges_[GBP/kWh]"
  ], enums.EnergyCharge.DAY_CHARGE.name)
  consumption_night_charges = ([
      "Consumption_charges", "Consumption_night_charges_[GBP/kWh]"
  ], enums.EnergyCharge.NIGHT_CHARGE.name)
  duos_red_charges = (["Distribution_charges", "DUoS_red_charges_[GBP/kWh]"],
                      enums.EnergyCharge.DUOS_RED.name)
  duos_amber_charges = ([
      "Distribution_charges", "DUoS_amber_charges_[GBP/kWh]"
  ], enums.EnergyCharge.DUOS_AMBER.name)
  duos_green_charges = ([
      "Distribution_charges", "DUoS_green_charges_[GBP/kWh]"
  ], enums.EnergyCharge.DUOS_GREEN.name)
  ccl = (["Charges_and_adjustments",
          "CCL_[GBP/kWh]"], enums.EnergyCharge.CCL.name)


@dataclass
class BaseExportElectricityPriceSchema:
  """Schema for export electricity price data."""
  export_revenues = (["Electricity_export_price_[GBP/kWh]"],
                     enums.EnergyCharge.ENERGY_CHARGE.name)


@dataclass
class BaseImportGasPriceSchema:
  """Schema for import gas price data."""
  export_revenues = (["consumption_charge_[GBP/kWh]"],
                     enums.EnergyCharge.ENERGY_CHARGE.name)
  ccl = (["CCL_[GBP/kWh]"], enums.EnergyCharge.CCL.name)


@dataclass
class BaseWindElectricityPriceSchema:
  """Schema for wind import electricity price data."""
  wind_charges = (["Onsite_electricity_generation_price_[GBP/kWh]"],
                  enums.EnergyCharge.ENERGY_CHARGE.name)
