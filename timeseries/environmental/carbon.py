from calendar import monthrange
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests

url = "https://api.carbonintensity.org.uk/intensity"


def get_current_emission():
  # Get the current emission
  response = requests.get(url)
  return response.json()


def get_emission_by_date(temp_date):
  # Get the emission by date
  temp_date = convert_datetime_to_isoformat(temp_date)
  response = requests.get(f'{url}/date/{temp_date}')
  return response.json()


def get_emission_by_date_range(start_date, end_date):
  # Get the emission by date range
  start_date = convert_datetime_to_isoformat(start_date)
  end_date = convert_datetime_to_isoformat(end_date)
  response = requests.get(f'{url}/{start_date}/{end_date}')
  return response.json()


def convert_datetime_to_isoformat(temp_date):
  # Convert the datetime to isoformat
  return temp_date.isoformat()


def json_response_to_dataframe(response: dict):

  # load the dictionary into a dataframe
  df = pd.DataFrame(response['data'])

  # select the desired columns
  df = df[['from', 'to', 'intensity']]

  # expand the nested dictionary into separate columns
  df = pd.concat(
      [df.drop(['intensity'], axis=1), df['intensity'].apply(pd.Series)],
      axis=1)
  return df


def get_number_days_in_month(year: int, month: int) -> int:
  # Get the number of days in a month

  return monthrange(year, month)[1]


def get_carbon_intensity_for_historical_year(year: int) -> pd.DataFrame:
  # Get the carbon intensity for a historical year
  frames = []
  for month in range(1, 13):
    nb_days = get_number_days_in_month(year, month)
    start_date = datetime(
        year,
        month,
        1,
        0,
        0,
    )
    end_date = datetime(year, month, nb_days, 23, 59)
    print(f'Getting data for {start_date} to {end_date} ...')
    response = get_emission_by_date_range(start_date, end_date)
    dataf = json_response_to_dataframe(response)
    frames.append(dataf)
  dataf = pd.concat(frames)
  return dataf


def main():
  year = 2022
  dataf = get_carbon_intensity_for_historical_year(year)
  filename = f'carbon_intensity_{year}.csv'
  dataf.to_csv(Path.cwd() / 'data' / filename, index=False)


if __name__ == "__main__":
  main()
