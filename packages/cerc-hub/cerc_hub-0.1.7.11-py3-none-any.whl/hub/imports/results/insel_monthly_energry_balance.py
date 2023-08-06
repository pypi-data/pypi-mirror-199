"""
Insel monthly energy balance
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guillermo.GutierrezMorote@concordia.ca
"""

from pathlib import Path
import pandas as pd
import csv
import hub.helpers.constants as cte


class InselMonthlyEnergyBalance:
  """
  Import SRA results
  """
  def __init__(self, city, base_path):

    self._city = city
    self._base_path = base_path

  @staticmethod
  def _conditioning_demand(insel_output_file_path):
    heating = []
    cooling = []
    with open(Path(insel_output_file_path).resolve()) as csv_file:
      csv_reader = csv.reader(csv_file)
      for line in csv_reader:
        demand = str(line).replace("['", '').replace("']", '').split()
        for i in range(0, 2):
          if demand[i] != 'NaN':
            aux = float(demand[i]) * 1000  # kWh to Wh
            demand[i] = str(aux)
          else:
            demand[i] = '0'
        heating.append(demand[0])
        cooling.append(demand[1])
    monthly_heating = pd.DataFrame(heating, columns=[cte.INSEL_MEB]).astype(float)
    monthly_cooling = pd.DataFrame(cooling, columns=[cte.INSEL_MEB]).astype(float)
    return monthly_heating, monthly_cooling

  def _dhw_demand(self):
    for building in self._city.buildings:
      domestic_hot_water_demand = []
      if building.internal_zones[0].thermal_zones is None:
        domestic_hot_water_demand = [0] * 12
      else:
        thermal_zone = building.internal_zones[0].thermal_zones[0]
        area = thermal_zone.total_floor_area
        cold_water = building.cold_water_temperature[cte.MONTH]['epw']
        for month in range(0, 12):
          total_dhw_demand = 0
          for schedule in thermal_zone.domestic_hot_water.schedules:
            total_day = 0
            for value in schedule.values:
              total_day += value
            for day_type in schedule.day_types:
              demand = thermal_zone.domestic_hot_water.peak_flow * cte.WATER_DENSITY * cte.WATER_HEAT_CAPACITY \
                       * (thermal_zone.domestic_hot_water.service_temperature - cold_water[month])
              total_dhw_demand += total_day * cte.DAYS_A_MONTH[day_type][month] * demand
          domestic_hot_water_demand.append(total_dhw_demand * area)

      building.domestic_hot_water_heat_demand[cte.MONTH] = \
        pd.DataFrame(domestic_hot_water_demand, columns=[cte.INSEL_MEB])

  def _electrical_demand(self):
    for building in self._city.buildings:
      lighting_demand = []
      appliances_demand = []
      if building.internal_zones[0].thermal_zones is None:
        lighting_demand = [0] * 12
        appliances_demand = [0] * 12
      else:
        thermal_zone = building.internal_zones[0].thermal_zones[0]
        area = thermal_zone.total_floor_area

        for month in range(0, 12):
          total_lighting = 0
          for schedule in thermal_zone.lighting.schedules:
            total_day = 0
            for value in schedule.values:
              total_day += value
            for day_type in schedule.day_types:
              total_lighting += total_day * cte.DAYS_A_MONTH[day_type][month] * thermal_zone.lighting.density
          lighting_demand.append(total_lighting * area)

          total_appliances = 0
          for schedule in thermal_zone.appliances.schedules:
            total_day = 0
            for value in schedule.values:
              total_day += value
            for day_type in schedule.day_types:
              total_appliances += total_day * cte.DAYS_A_MONTH[day_type][month] * thermal_zone.appliances.density
          appliances_demand.append(total_appliances * area)

      building.lighting_electrical_demand[cte.MONTH] = pd.DataFrame(lighting_demand, columns=[cte.INSEL_MEB])
      building.appliances_electrical_demand[cte.MONTH] = pd.DataFrame(appliances_demand, columns=[cte.INSEL_MEB])

  def enrich(self):
    for building in self._city.buildings:
      file_name = building.name + '.out'
      insel_output_file_path = Path(self._base_path / file_name).resolve()
      if insel_output_file_path.is_file():
        building.heating[cte.MONTH], building.cooling[cte.MONTH] = self._conditioning_demand(insel_output_file_path)
        building.heating[cte.YEAR] = pd.DataFrame(
          [building.heating[cte.MONTH][cte.INSEL_MEB].astype(float).sum()], columns=[cte.INSEL_MEB]
        )
        building.cooling[cte.YEAR] = pd.DataFrame(
          [building.cooling[cte.MONTH][cte.INSEL_MEB].astype(float).sum()], columns=[cte.INSEL_MEB]
        )
    self._dhw_demand()
    self._electrical_demand()
