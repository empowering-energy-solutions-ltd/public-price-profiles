import copy
from datetime import date, datetime, time, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from timeseries.common import datetime_functions, enums
from timeseries.data import schema
from timeseries.economic import tariff_structure


def create_duos_electricity_charges(**args) -> pd.Series:
  """Create a Series to represent the DUOS charges for electricity.
  Date is the date of the charges
  Green_charges is in £/kWh
  Amber_charges is in £/kWh
  Red_charges is in £/kWh

  Sets the charges for the green band, amber band and red band for given times of the day.
  """
  temp_date = args["Date"].date()
  green_charges = args[schema.DataInputSchema.DUOS_GREEN]
  amber_charges = args[schema.DataInputSchema.DUOS_AMBER]
  red_charges = args[schema.DataInputSchema.DUOS_RED]

  temp_series = get_date_range(temp_date)
  time_index = temp_series.index.time
  day_of_week_index = temp_series.index.day_of_week

  temp_series.loc[:] = green_charges  # green price
  period_filter_red_band = ((day_of_week_index < 5)
                            & (time_index >= time(16, 00))
                            & (time_index < time(19, 00)))
  temp_series.loc[period_filter_red_band] = red_charges  # red price
  period_filter_amber_band = ((day_of_week_index < 5)
                              & (time_index >= time(7, 00))
                              & (time_index < time(16, 00)))
  temp_series.loc[period_filter_amber_band] = amber_charges  # amber price
  period_filter_amber_band = ((day_of_week_index < 5)
                              & (time_index >= time(19, 00))
                              & (time_index < time(23, 00)))
  temp_series.loc[period_filter_amber_band] = amber_charges  # amber price

  return temp_series


def create_duos_gas_charges(**args):
  """Create a Series to represent the DUOS charges for gas. Which is the same for all times of the day."""
  temp_date = args["Date"].date()
  gas_charges = args[schema.DataInputSchema.GAS_CHARGE]

  temp_series = get_date_range(temp_date)
  temp_series.loc[:] = gas_charges  # green price

  return temp_series


def create_series_with_default_value(default_value_col: str, **args):
  temp_date = args["Date"].date()
  default_value_col = args[default_value_col]
  temp_series = get_date_range(temp_date)
  temp_series.fillna(default_value_col, inplace=True)
  return temp_series


def create_day_night_series(**args) -> pd.Series:
  """Create a Series to represent a day/night tariff.
    Day tariff is set to be between 7 am and 12pm.
    Day_charges is in £/kWh
    Night_charges is in £/kWh"""
  temp_date = args["Date"].date()
  day_charges = args[schema.DataInputSchema.DAY_CHARGE]
  night_charges = args[schema.DataInputSchema.NIGHT_CHARGE]

  temp_series = get_date_range(temp_date)
  time_index = temp_series.index.time
  temp_series.loc[:] = night_charges
  period_filter_day_charges = time_index >= time(7, 00)
  temp_series.loc[period_filter_day_charges] = day_charges
  return temp_series


def create_import_gas_tariff_structure_from_data(
    dataf: pd.DataFrame, ) -> tariff_structure.TariffStructure:
  """Create a tariff structure based on the value of a dataframe compliant with the gas import schema."""
  dataf = dataf.reset_index()
  ccl_charges = pd.concat([
      create_series_with_default_value(schema.DataInputSchema.CCL, **args)
      for args in dataf.to_dict("records")
  ])
  climate_change_levy = tariff_structure.ConsumptionCharges(
      schema.DataInputSchema.CCL, ccl_charges)

  gas_charges = pd.concat([
      create_series_with_default_value(schema.DataInputSchema.ENERGY_CHARGE,
                                       **args)
      for args in dataf.to_dict("records")
  ])
  climate_change_levy = tariff_structure.ConsumptionCharges(
      schema.DataInputSchema.CCL, ccl_charges)
  gas_price = tariff_structure.ConsumptionCharges(
      schema.DataInputSchema.ENERGY_CHARGE, gas_charges)

  list_charges = [climate_change_levy, gas_price]

  gas_tariff_structure = tariff_structure.TariffStructure(
      energy_carrier=enums.EnergyCarrier.NATURALGAS,
      destination=enums.Destination.IMPORT,
      origin=enums.TechnologyType.GRID,
      list_consumption_charges=list_charges,
  )
  return gas_tariff_structure


def create_import_electricity_tariff_structure_from_data(
    dataf: pd.DataFrame, ) -> tariff_structure.TariffStructure:
  """Create a tariff structure based on the value of a dataframe compliant with the electricity import schema."""
  dataf = dataf.reset_index()
  day_night_charges = pd.concat(
      [create_day_night_series(**args) for args in dataf.to_dict("records")])
  ccl_charges = pd.concat([
      create_series_with_default_value(schema.DataInputSchema.CCL, **args)
      for args in dataf.to_dict("records")
  ])
  duos_charges = pd.concat([
      create_duos_electricity_charges(**args)
      for args in dataf.to_dict("records")
  ])
  climate_change_levy = tariff_structure.ConsumptionCharges(
      schema.DataInputSchema.CCL, ccl_charges)

  duos_charges = tariff_structure.ConsumptionCharges(
      schema.DataInputSchema.DUOS, duos_charges)

  electricity_price = tariff_structure.ConsumptionCharges(
      schema.DataInputSchema.ENERGY_CHARGE, day_night_charges)
  list_charges = [climate_change_levy, duos_charges, electricity_price]

  electricity_tariff_structure = tariff_structure.TariffStructure(
      energy_carrier=enums.EnergyCarrier.ELECTRICITY,
      destination=enums.Destination.IMPORT,
      origin=enums.TechnologyType.GRID,
      list_consumption_charges=list_charges,
  )

  return electricity_tariff_structure


def create_default_import_gas_data(start_datetime: datetime,
                                   end_datetime: datetime) -> pd.DataFrame:
  """Create a dataframe filled with default import gas prices values"""
  index = pd.date_range(start_datetime, end_datetime, freq="MS")
  ccl = 0.00568
  gas_charges = 0.0258  # for 2022 in QEH
  price_dict = {
      schema.DataInputSchema.ENERGY_CHARGE: [gas_charges],
      schema.DataInputSchema.CCL: [ccl],
  }

  return create_dataframe_from_dict(price_dict, index)


def create_dataframe_from_dict(input_dict: dict[str, list[float]],
                               index: pd.DatetimeIndex) -> pd.DataFrame:
  """Create a default price dataframe."""
  default_price_dataf = pd.DataFrame.from_dict(input_dict)
  default_price_dataf = default_price_dataf.iloc[[0] * len(index)]
  default_price_dataf.index = index
  default_price_dataf.index.name = "Date"
  return default_price_dataf


def create_default_import_electricity_data(
    start_datetime: datetime, end_datetime: datetime) -> pd.DataFrame:
  """Create a dataframe filled with default import electricity prices values"""
  index = pd.date_range(start_datetime, end_datetime, freq="MS")
  # for 2022
  ccl = 0.00775
  night_charges = 0.113827
  day_charges = 0.138323
  red_charges = 0.0557
  green_charges = 0.00035
  amber_charges = 0.0018
  price_dict = {
      schema.DataInputSchema.CCL: [ccl],
      schema.DataInputSchema.DAY_CHARGE: [day_charges],
      schema.DataInputSchema.NIGHT_CHARGE: [night_charges],
      schema.DataInputSchema.DUOS_RED: [red_charges],
      schema.DataInputSchema.DUOS_GREEN: [green_charges],
      schema.DataInputSchema.DUOS_AMBER: [amber_charges],
  }
  return create_dataframe_from_dict(price_dict, index)


def create_default_import_gas_tariff_structure(
    start_datetime: datetime,
    end_datetime: datetime) -> tariff_structure.TariffStructure:
  """Create default import gas tariff structure."""
  price_dataf = create_default_import_gas_data(start_datetime, end_datetime)
  return create_import_gas_tariff_structure_from_data(price_dataf)


def create_default_import_electricity_tariff_structure(
    start_datetime: datetime,
    end_datetime: datetime) -> tariff_structure.TariffStructure:
  """Create default import electricity tariff structure."""
  price_dataf = create_default_import_electricity_data(start_datetime,
                                                       end_datetime)
  return create_import_electricity_tariff_structure_from_data(price_dataf)


def filter_input_data(dataf: pd.DataFrame, start_time: datetime,
                      end_time: datetime):
  """Filter the input data to the given time range."""
  filt = (dataf.index >= start_time) & (dataf.index <= end_time)
  return dataf.loc[filt]


def create_hh_dataframe(org_hh_df: pd.DataFrame, start_month: date,
                        end_month: date) -> pd.DataFrame:
  """Create a half-hourly dataframe for the given date based on the average weeks values from the input dataframe."""
  new_index = pd.date_range(start_month, end_month, freq="MS")
  frames = []
  for datetime_month in new_index:
    temp_df = get_date_range(datetime_month).to_frame()
    temp_df = datetime_functions.add_time_features(temp_df).dropna(
        axis=1).reset_index()
    temp_df["Key"] = (temp_df["Week"] * 7 * 48 + temp_df["Day_of_week"] * 48 +
                      temp_df["HH"])
    lookup_dict = get_average_week(org_hh_df)
    for col in org_hh_df.columns:
      temp_df = pd.merge(temp_df,
                         lookup_dict[col],
                         left_on="Key",
                         right_on="Key")

    temp_df = temp_df.set_index("index")[org_hh_df.columns]
    frames.append(temp_df)

  return pd.concat(frames, axis=0)


def get_date_range(target_month: date) -> pd.Series:
  """Create a series with a date range for the given month."""
  start_time = datetime.combine(target_month, time(0, 0)).replace(day=1)
  end_time = (start_time +
              timedelta(days=32)).replace(day=1) - timedelta(minutes=30)
  return pd.Series(index=pd.date_range(start_time, end_time, freq="30min"),
                   data=np.nan)


def get_average_week(dataf: pd.DataFrame) -> dict[str, pd.DataFrame]:
  """Return a dictionary of the average week values for each column."""
  org_columns = dataf.columns
  dataf = datetime_functions.add_time_features(dataf)
  dataf[
      "Key"] = dataf["Week"] * 7 * 48 + dataf["Day_of_week"] * 48 + dataf["HH"]
  avg_week_dict = {}
  for col in org_columns:
    temp_dataf = dataf.groupby(["Key"]).agg({col: ["mean"]})
    temp_dataf.columns = [col]
    avg_week_dict[col] = temp_dataf
  return avg_week_dict


def shift_filter_monthly_dataframe(org_monthly_df: pd.DataFrame,
                                   start_month: date,
                                   end_month: date) -> pd.DataFrame:
  """Create a dataframe for a period where the last available price data is used."""
  org_monthly_df.sort_index(ascending=False, inplace=True)
  shifted_monthly_data = []
  new_index = pd.date_range(start_month, end_month, freq="MS")
  for datetime_month in new_index:
    filt = org_monthly_df.index.month == datetime_month.month
    shifted_monthly_data.append(org_monthly_df.loc[filt].head(1).values[0])

  new_df = pd.DataFrame(shifted_monthly_data,
                        index=new_index,
                        columns=org_monthly_df.columns)
  new_df.index.name = org_monthly_df.index.name
  return new_df


def get_attributes_class(input_class: object) -> dict:
  """Return a list of the attributes of a class."""
  dict_attributes = input_class.__dict__
  dict_attributes = {k: v for k, v in dict_attributes.items()}
  final_dict = copy.copy(dict_attributes)
  for k in dict_attributes:
    if k[0] == "_":
      final_dict.pop(k)
  return final_dict


def get_columns_from_schema(input_class: object) -> list:
  """Return the name of the columns."""
  dict_attributes = get_attributes_class(input_class)
  return [
      tuple(v[0]) if len(v[0]) > 1 else v[0][0]
      for v in dict_attributes.values()
  ]


def get_rename_columns_dict(input_class: object) -> dict:
  """Return a dictionary of the columns names."""
  dict_attributes = get_attributes_class(input_class)
  list_keys = get_columns_from_schema(input_class)
  list_values = [v[1] for v in dict_attributes.values()]
  return {k: v for k, v in zip(list_keys, list_values)}


def rename_columns(dataf: pd.DataFrame, rename_dict: dict) -> pd.DataFrame:
  dataf.columns = [rename_dict[col_name] for col_name in dataf.columns]
  return dataf


def add_date_index(dataf: pd.DataFrame):
  """Add date index to the price data."""
  dataf.index.names = ["Year", "Month"]
  dataf.reset_index(inplace=True)
  dataf["Day"] = 1
  dataf.index = pd.to_datetime(dataf[["Year", "Month", "Day"]])
  dataf.drop(["Year", "Month", "Day"], axis=1, inplace=True)
  dataf.index.name = "Date"
  return dataf


def transform_hh_price_data(dataf: pd.DataFrame(),
                            base_schema: object) -> pd.DataFrame:
  """Return a dataframe of the input half-houlry price dataframe standardised."""
  list_columns_to_import = get_columns_from_schema(base_schema)
  dataf = dataf[list_columns_to_import].dropna()
  rename_dict = get_rename_columns_dict(base_schema)
  dataf = dataf.pipe(rename_columns, rename_dict)
  return dataf


def transform_monthly_price_data(dataf: pd.DataFrame(),
                                 base_schema: object) -> pd.DataFrame:
  """Return a dataframe of the input monthly price dataframe standardised."""

  list_columns_to_import = get_columns_from_schema(base_schema)
  dataf = dataf[list_columns_to_import].dropna()
  rename_dict = get_rename_columns_dict(base_schema)
  dataf = dataf.pipe(rename_columns, rename_dict).pipe(add_date_index)
  return dataf


def import_price_data(
    path_to_data: Path,
    index_col: list[int] | None = None,
    header: list[int] | None = None,
    sheet_name: str | None = None,
) -> pd.DataFrame:
  """Return a dataframe of the price data."""
  if index_col is None:
    index_col = [0]
  if header is None:
    header = [0]
  if sheet_name is None:
    dataf = pd.read_csv(path_to_data, index_col=index_col, header=header)
  else:
    dataf = pd.read_excel(path_to_data,
                          index_col=index_col,
                          header=header,
                          sheet_name=sheet_name)
  return dataf
