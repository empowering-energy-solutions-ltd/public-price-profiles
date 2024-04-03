class DataSchema:
  DATE = "Datetime"
  ID = "ID"
  VALUE = "Value"


class MetadataSchema:
  """Schema used to ensure that the metadata information is fully and correclty filled."""

  ENERGY_CARRIER = "energy_carrier"
  UNIT = "Unit"
  ORG_NAME = "original_name"
  ORIGIN_ENTITY_ID = "origin_ID"
  DESTINATION_ENTITY_ID = (
      "destination_ID"  # if origin_ID == destination_ID it is an energy demand
  )
  PROFILE_ID = DataSchema.ID
  TYPE = "Type_of_profile"


class StructureSchema:
  UNIT_ID = "Unit_ID"
  INPUT_ENERGY_CARRIER = "Input_energy_carrier"
  OUTPUT_ENERGY_CARRIER = "Output_energy_carrier"
  ORIGIN_ENTITY_ID = "Origin_entity_ID"
  DESTINATION_ENTITY_ID = "Destination_entity_ID"
  TYPE = "Type"


class ResultsSchema:
  DESTINATION = "Destination"
  ENERGY_CARRIER = "Energy carrier"
  UNIT = "Unit"
  INDEX = "Datetime_UTC"
  NAME = "Name of unit"
  ORIGIN = "Origin"


class TariffSchema:
  YEAR = "Year"
  Month = "Month"
  CCL = "CCL"


class DataInputSchema:
  """Input schema used to create tariff structure object"""
  INDEX = "Date"
  METERCODE = 'MPAN/MPR'
  CCL = 'CCL'
  DAY_CHARGE = 'DAY_CHARGE'
  NIGHT_CHARGE = 'NIGHT_CHARGE'
  DUOS_RED = 'DUOS_RED'
  DUOS_AMBER = 'DUOS_AMBER'
  DUOS_GREEN = 'DUOS_GREEN'
  GAS = 'GAS_CHARGE'
  ENERGY_CHARGE = 'Energy_Charge'
  DUOS = 'DUOS'


class EDFImportSchema:
  BY_BILL_PERIOD = 'ByBillPeriod'
  DETAILED = 'DetailedEnergy'
  NON_DETAILED = 'DetailedNonEnergy'

  BILL_PERIOD = 'Bill Period Start Date'
  BILL_PERIOD_2 = 'Bill Period\nStart Date'
  CONSUMP_KWH = 'Consumption\nkWh'
  CCL_AMOUNT = 'CCL\nAmount'
  RATE_RATE = 'Rate'
  RATE_DESCRIPT = f'{RATE_RATE} Description'
  RATE_CONSUMPT = f'{RATE_RATE}\nConsumption'
  RATE_CHARGE = f'{RATE_RATE}\nCharge'
  ENERGY_CHARGE = 'Energy Charge (kWh)'
  DAY_E_CHARGE = f'{ENERGY_CHARGE} - Day'
  NIGHT_E_CHARGE = f'{ENERGY_CHARGE} - Night'
  DEMAND_CHARGE = 'Demand Charge'
  RED = 'Red'
  AMBER = 'Amber'
  GREEN = 'Green'
  RED_CONSUMP = f'{RED} Consumption kWh'
  RED_CHARGE = f'{RED}\nCharge'
  AMBER_CONSUMP = f'{AMBER} Consumption kWh'
  AMBER_CHARGE = f'{AMBER} Charge'
  GREEN_CONSUMP = f'{GREEN} Consumption kWh'
  GREEN_CHARGE = f'{GREEN}\nCharge'


class ImportElecSchema:
  INFO = 'Invoice information'
  DISTRIBUTION = 'Distribution consumption'
  SUPPLY = 'Supply consumption charges'

  ID = 'mpan'
  START_DATE = 'start_date'
  END_DATE = 'end_date'
  DATE = 'Date'
  CHARGE = 'Charge rate (£/kWh)'
  RED = f'Red - {CHARGE}'
  AMBER = f'Amber - {CHARGE}'
  GREEN = f'Green - {CHARGE}'
  DAY = f'Day - {CHARGE}'
  NIGHT = f'Night - {CHARGE}'
  CARBON = 'Carbon Tax'
  ACCOUNT = 'Account ID'


class ImportGasSchema:
  START_DATE = 'period_from'
  ID = 'mpr'
  CARBON = 'ccl_rate_per_kWh'
  GAS_RATE = 'charge_rate_per_kWh'
