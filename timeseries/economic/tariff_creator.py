from timeseries.common import enums
from dataclasses import dataclass, field
import pandas as pd
from pathlib import Path
from timeseries.data import schema
from datetime import timedelta, datetime
from timeseries.economic import tariff_functions, tariff_structure


@dataclass
class EnergyTariffImporter:
  """Class to import and filter energy tariff data.
  Args:
      name: str
        A name for the class object
      invoice_data_dict: dict[enums.EnergyCarrier, pd.DataFrame] = field(default_factory=dict)
        A dictionary with the energy carrier as the key and the tariff data as the value.
  
  Methods:
      load_data(invoice_path_dict: dict[enums.EnergyCarrier, Path]) -> None:
          Load data from a dictionary of paths.
      rename_columns_electricity_data(elec_dataf: pd.DataFrame) -> pd.DataFrame:
          Rename the columns of the electricity data.
      import_electricity_data(org_dataf: pd.DataFrame) -> pd.DataFrame:
          Import the electricity data.
      rename_columns_gas_data(gas_dataf: pd.DataFrame) -> pd.DataFrame:
          Rename the columns of the gas data.
      import_gas_data(org_dataf: pd.DataFrame) -> pd.DataFrame:
          Import the gas data.
      get_all_meter_ids() -> dict[enums.EnergyCarrier, list[int]]:
          Get all the meter ids.
      find_meter(meter_id: int) -> enums.EnergyCarrier:
          Find the meter id.
      filter_data(meter_id: int | None = None, start_date: datetime | None = None, end_date: datetime | None = None) -> pd.DataFrame:
          Filter the data.
      get_tariff_structure(meter_id: int, start_date: datetime | None = None, end_date: datetime | None = None) -> tariff_structure.TariffStructure | None:
          Get the tariff structure.
  """
  name: str
  invoice_data_dict: dict[enums.EnergyCarrier,
                          pd.DataFrame] = field(default_factory=dict)

  def load_data(self, invoice_path_dict: dict[enums.EnergyCarrier, Path]):
    invoice_data = {}
    for energy_carrier, temp_path in invoice_path_dict.items():
      if energy_carrier is enums.EnergyCarrier.ELECTRICITY:
        temp_dataf = pd.read_csv(temp_path, header=[0, 1], index_col=None)
        temp_dataf = self.import_electricity_data(temp_dataf)
      elif energy_carrier is enums.EnergyCarrier.NATURALGAS:
        temp_dataf = pd.read_csv(temp_path)
        temp_dataf = self.import_gas_data(temp_dataf)
      else:
        raise ValueError(
            "Utility type must be enums.EnergyCarrier.ELECTRICITY or .NATURALGAS. Re-enter utility type."
        )
      invoice_data[energy_carrier] = temp_dataf
    self.invoice_data_dict = invoice_data

  def rename_columns_electricity_data(
      self, elec_dataf: pd.DataFrame) -> pd.DataFrame:
    rename_dict = {
        schema.ImportElecSchema.ID: schema.DataInputSchema.METERCODE,
        schema.ImportElecSchema.CHARGE: schema.DataInputSchema.CCL,
        schema.ImportElecSchema.GREEN: schema.DataInputSchema.DUOS_GREEN,
        schema.ImportElecSchema.RED: schema.DataInputSchema.DUOS_RED,
        schema.ImportElecSchema.AMBER: schema.DataInputSchema.DUOS_AMBER,
        schema.ImportElecSchema.DAY: schema.DataInputSchema.DAY_CHARGE,
        schema.ImportElecSchema.NIGHT: schema.DataInputSchema.NIGHT_CHARGE,
    }
    elec_dataf.index.name = schema.DataInputSchema.INDEX
    return elec_dataf.rename(columns=rename_dict)

  def import_electricity_data(self, org_dataf: pd.DataFrame) -> pd.DataFrame:

    try:
      org_dataf.index = pd.to_datetime(
          org_dataf[schema.ImportElecSchema.INFO][
              schema.ImportElecSchema.START_DATE],
          format="%Y-%m-%d",
      )
    except ValueError:
      org_dataf.index = pd.to_datetime(
          org_dataf[schema.ImportElecSchema.INFO][
              schema.ImportElecSchema.START_DATE],
          format="%d/%m/%Y",
      )
    cols_to_drop = [
        schema.ImportElecSchema.START_DATE, schema.ImportElecSchema.END_DATE
    ]
    org_dataf.drop(
        cols_to_drop,
        axis="columns",
        level=1,
        inplace=True,
    )
    elec_raw = org_dataf.loc[:, [
        (schema.ImportElecSchema.INFO, schema.ImportElecSchema.ID),
        (schema.ImportElecSchema.CARBON, schema.ImportElecSchema.CHARGE),
        (
            schema.ImportElecSchema.DISTRIBUTION,
            schema.ImportElecSchema.GREEN,
        ),
        (
            schema.ImportElecSchema.DISTRIBUTION,
            schema.ImportElecSchema.AMBER,
        ),
        (
            schema.ImportElecSchema.DISTRIBUTION,
            schema.ImportElecSchema.RED,
        ),
        (
            schema.ImportElecSchema.SUPPLY,
            schema.ImportElecSchema.DAY,
        ),
        (
            schema.ImportElecSchema.SUPPLY,
            schema.ImportElecSchema.NIGHT,
        ),
    ], ].copy()
    elec_raw.columns = elec_raw.columns.droplevel()
    elec_raw = self.rename_columns_electricity_data(elec_raw)
    return elec_raw

  def rename_columns_gas_data(self, gas_dataf: pd.DataFrame) -> pd.DataFrame:
    rename_dict = {
        schema.ImportGasSchema.ID: schema.DataInputSchema.METERCODE,
        schema.ImportGasSchema.CARBON: schema.DataInputSchema.CCL,
        schema.ImportGasSchema.GAS_RATE: schema.DataInputSchema.ENERGY_CHARGE
    }
    gas_dataf.index.name = schema.DataInputSchema.INDEX
    return gas_dataf.rename(columns=rename_dict)

  def import_gas_data(self, org_dataf: pd.DataFrame) -> pd.DataFrame:
    gas_raw = org_dataf[[
        schema.ImportGasSchema.START_DATE,
        schema.ImportGasSchema.ID,
        schema.ImportGasSchema.CARBON,
        schema.ImportGasSchema.GAS_RATE,
    ]].copy()

    gas_raw.index = pd.to_datetime(gas_raw[schema.ImportGasSchema.START_DATE],
                                   format="%Y-%m-%d") + timedelta(1)
    gas_raw.drop(schema.ImportGasSchema.START_DATE,
                 axis="columns",
                 inplace=True)
    return self.rename_columns_gas_data(gas_raw)

  def get_all_meter_ids(self) -> dict[enums.EnergyCarrier, list[int]]:
    dict_meter_ids = {}
    for energy_carrier, temp_dataf in self.invoice_data_dict.items():
      dict_meter_ids[energy_carrier] = list(
          temp_dataf[schema.DataInputSchema.METERCODE].unique())
    return dict_meter_ids

  def find_meter(self, meter_id: int) -> enums.EnergyCarrier:
    all_meters = self.get_all_meter_ids()
    for energy_carrier, list_meters in all_meters.items():
      if meter_id in list_meters:
        return energy_carrier
    return enums.EnergyCarrier.NONE

  def filter_data(self,
                  meter_id: int | None = None,
                  start_date: datetime | None = None,
                  end_date: datetime | None = None):
    dataf = pd.DataFrame()

    if meter_id is not None:
      energy_carrier = self.find_meter(meter_id)
      if energy_carrier is not enums.EnergyCarrier.NONE:
        dataf = self.invoice_data_dict[energy_carrier].copy()
        dataf = dataf.sort_index()
        if start_date is None:
          start_date = dataf.index[0]
        if end_date is None:
          end_date = dataf.index[-1]
        filt = (dataf[schema.DataInputSchema.METERCODE] == meter_id) & (
            dataf.index >= start_date) & (dataf.index <= end_date)
        dataf = dataf.loc[filt]
    return dataf

  def get_tariff_structure(
      self,
      meter_id: int,
      start_date: datetime | None = None,
      end_date: datetime | None = None
  ) -> tariff_structure.TariffStructure | None:
    energy_carrier = self.find_meter(meter_id)
    if energy_carrier is not enums.EnergyCarrier.NONE:
      dataf = self.filter_data(meter_id, start_date, end_date)
      if energy_carrier is enums.EnergyCarrier.ELECTRICITY:
        return tariff_functions.create_import_electricity_tariff_structure_from_data(
            dataf)
      elif energy_carrier is enums.EnergyCarrier.NATURALGAS:
        return tariff_functions.create_import_gas_tariff_structure_from_data(
            dataf)
    return None
