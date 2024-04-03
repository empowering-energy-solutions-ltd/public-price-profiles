from datetime import datetime
import pandas as pd


def get_list_months_per_year(start_datetime: datetime,
                             end_datetime: datetime) -> dict[int:list[int]]:
  """Return a dict with keys being years and values being the list of months in between two datetimes."""
  start_year = start_datetime.year
  end_year = end_datetime.year
  dict_results = {}
  for year in range(start_year, end_year + 1):
    if year == start_year:
      temp_start_month = start_datetime.month
    else:
      temp_start_month = 1
    if year == end_year:
      temp_end_month = end_datetime.month
    else:
      temp_end_month = 12
    dict_results[year] = [
        x for x in range(temp_start_month, temp_end_month + 1)
    ]
  return dict_results


def add_time_features(dataf: pd.DataFrame) -> pd.DataFrame:
  """Add time features to a dataframe."""
  new_dataf = dataf.copy()
  season_dict = {
      "Winter": 1,
      "Spring": 2,
      "Summer": 3,
      "High Summer": 4,
      "Autumn": 5
  }

  new_dataf["Hour"] = new_dataf.index.hour
  new_dataf["Day_of_week"] = new_dataf.index.dayofweek
  new_dataf["Day"] = new_dataf.index.dayofyear
  new_dataf["Month"] = new_dataf.index.month
  new_dataf["Year"] = new_dataf.index.year
  new_dataf["Weekday_flag"] = [
      "weekday" if x < 5 else "weekend" for x in new_dataf.index.dayofweek
  ]
  new_dataf["HH"] = new_dataf.index.hour * 2 + new_dataf.index.minute // 30
  new_dataf["HH"] = new_dataf["HH"].astype(int)
  new_dataf["Date"] = new_dataf.index.date
  new_dataf["Week"] = new_dataf.index.isocalendar().week
  return new_dataf
