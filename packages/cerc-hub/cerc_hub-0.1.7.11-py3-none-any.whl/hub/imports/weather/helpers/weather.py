"""
weather helper
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import math
import hub.helpers.constants as cte
import pandas as pd
import calendar as cal
import numpy as np


class Weather:
  """
  Weather class
  """

  @staticmethod
  def sky_temperature(ambient_temperature):
    """
    Get sky temperature from ambient temperature in Celsius
    :return: List[float]
    """
    # Swinbank - Source sky model approximation(1963) based on cloudiness statistics(32 %) in United States
    # ambient temperatures( in °C)
    # sky temperatures( in °C)
    values = []
    for temperature in ambient_temperature:
      value = 0.037536 * math.pow((temperature + cte.KELVIN), 1.5) \
              + 0.32 * (temperature + cte.KELVIN) - cte.KELVIN
      values.append(value)
    return values

  @staticmethod
  def cold_water_temperature(ambient_temperature):
    """
    Get cold water temperature from ambient temperature in Celsius
    :return: dict
    """
    # Equation from "TOWARDS DEVELOPMENT OF AN ALGORITHM FOR MAINS WATER TEMPERATURE", 2004, Jay Burch
    # and Craig Christensen, National Renewable Energy Laboratory
    # ambient temperatures( in °C)
    # cold water temperatures( in °C)
    ambient_temperature_fahrenheit = []
    average_temperature = 0
    maximum_temperature = -1000
    minimum_temperature = 1000
    for temperature in ambient_temperature:
      value = temperature * 9 / 5 + 32
      ambient_temperature_fahrenheit.append(value)
      average_temperature += value / 8760
      if value > maximum_temperature:
        maximum_temperature = value
      if value < minimum_temperature:
        minimum_temperature = value
    delta_temperature = maximum_temperature - minimum_temperature
    ratio = 0.4 + 0.01 * (average_temperature - 44)
    lag = 35 - 1 * (average_temperature - 44)
    cold_temperature = []
    for temperature in ambient_temperature_fahrenheit:
      radians = (0.986 * (temperature-15-lag) - 90) * math.pi / 180
      cold_temperature.append((average_temperature + 6 + ratio * (delta_temperature/2) * math.sin(radians) - 32) * 5/9)
    return pd.DataFrame(cold_temperature, columns=['epw'])

  def get_monthly_mean_values(self, values):
    out = None
    if values is not None:
      if 'month' not in values.columns:
        values = pd.concat([self.month_hour, pd.DataFrame(values)], axis=1)
      out = values.groupby('month', as_index=False).mean()
      del out['month']
    return out

  @staticmethod
  def get_yearly_mean_values(values):
    return values.mean()

  def get_total_month(self, values):
    out = None
    if values is not None:
      if 'month' not in values.columns:
        values = pd.concat([self.month_hour, pd.DataFrame(values)], axis=1)
      out = pd.DataFrame(values).groupby('month', as_index=False).sum()
      del out['month']
    return out

  @property
  def month_hour(self):
    """
    returns a DataFrame that has x values of the month number (January = 1, February = 2...),
    being x the number of hours of the corresponding month
    :return: DataFrame(int)
    """
    array = []
    for i in range(0, 12):
      days_of_month = cal.monthrange(2015, i+1)[1]
      total_hours = days_of_month * 24
      array = np.concatenate((array, np.full(total_hours, i + 1)))
    return pd.DataFrame(array, columns=['month'])
