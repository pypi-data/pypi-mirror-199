"""
NrcanUsageParameters extracts the usage properties from NRCAN catalog and assigns to each building
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import sys

from hub.hub_logger import logger
import hub.helpers.constants as cte
from hub.helpers.dictionaries import Dictionaries
from hub.city_model_structure.building_demand.usage import Usage
from hub.city_model_structure.building_demand.lighting import Lighting
from hub.city_model_structure.building_demand.occupancy import Occupancy
from hub.city_model_structure.building_demand.appliances import Appliances
from hub.city_model_structure.building_demand.thermal_control import ThermalControl
from hub.city_model_structure.building_demand.domestic_hot_water import DomesticHotWater
from hub.catalog_factories.usage_catalog_factory import UsageCatalogFactory


class NrcanUsageParameters:
  """
  NrcanUsageParameters class
  """
  def __init__(self, city, base_path):
    self._city = city
    self._path = base_path

  def enrich_buildings(self):
    """
    Returns the city with the usage parameters assigned to the buildings
    :return:
    """
    city = self._city
    nrcan_catalog = UsageCatalogFactory('nrcan').catalog
    comnet_catalog = UsageCatalogFactory('comnet').catalog

    for building in city.buildings:
      usage_name = Dictionaries().hub_usage_to_nrcan_usage[building.function]
      try:
        archetype_usage = self._search_archetypes(nrcan_catalog, usage_name)
      except KeyError:
        logger.error(f'Building {building.name} has unknown usage archetype for usage: {usage_name}\n')
        sys.stderr.write(f'Building {building.name} has unknown usage archetype for usage: {usage_name}\n')
        continue

      usage_name = Dictionaries().hub_usage_to_comnet_usage[building.function]
      try:
        comnet_archetype_usage = self._search_archetypes(comnet_catalog, usage_name)
      except KeyError:
        logger.error(f'Building {building.name} has unknown usage archetype for usage: {usage_name}\n')
        sys.stderr.write(f'Building {building.name} has unknown usage archetype for usage: {usage_name}\n')
        continue

      for internal_zone in building.internal_zones:
        if internal_zone.area is None:
          raise Exception('Internal zone area not defined, ACH cannot be calculated')
        if internal_zone.volume is None:
          raise Exception('Internal zone volume not defined, ACH cannot be calculated')
        if internal_zone.area <= 0:
          raise Exception('Internal zone area is zero, ACH cannot be calculated')
        volume_per_area = internal_zone.volume / internal_zone.area
        usage = Usage()
        usage.name = usage_name
        self._assign_values(usage, archetype_usage, volume_per_area, building.cold_water_temperature)
        self._assign_comnet_extra_values(usage, comnet_archetype_usage, archetype_usage.occupancy.occupancy_density)
        usage.percentage = 1
        self._calculate_reduced_values_from_extended_library(usage, archetype_usage)

        internal_zone.usages = [usage]

  @staticmethod
  def _search_archetypes(catalog, usage_name):
    archetypes = catalog.entries('archetypes').usages
    for building_archetype in archetypes:
      if str(usage_name) == str(building_archetype.name):
        return building_archetype
    raise KeyError('archetype not found')

  @staticmethod
  def _assign_values(usage, archetype, volume_per_area, cold_water_temperature):
    if archetype.mechanical_air_change > 0:
      usage.mechanical_air_change = archetype.mechanical_air_change
    elif archetype.ventilation_rate > 0:
      usage.mechanical_air_change = archetype.ventilation_rate / volume_per_area * cte.HOUR_TO_SECONDS
    else:
      usage.mechanical_air_change = 0
    _occupancy = Occupancy()
    _occupancy.occupancy_density = archetype.occupancy.occupancy_density
    _occupancy.sensible_radiative_internal_gain = archetype.occupancy.sensible_radiative_internal_gain
    _occupancy.latent_internal_gain = archetype.occupancy.latent_internal_gain
    _occupancy.sensible_convective_internal_gain = archetype.occupancy.sensible_convective_internal_gain
    _occupancy.occupancy_schedules = archetype.occupancy.schedules
    usage.occupancy = _occupancy
    _lighting = Lighting()
    _lighting.density = archetype.lighting.density
    _lighting.convective_fraction = archetype.lighting.convective_fraction
    _lighting.radiative_fraction = archetype.lighting.radiative_fraction
    _lighting.latent_fraction = archetype.lighting.latent_fraction
    _lighting.schedules = archetype.lighting.schedules
    usage.lighting = _lighting
    _appliances = Appliances()
    _appliances.density = archetype.appliances.density
    _appliances.convective_fraction = archetype.appliances.convective_fraction
    _appliances.radiative_fraction = archetype.appliances.radiative_fraction
    _appliances.latent_fraction = archetype.appliances.latent_fraction
    _appliances.schedules = archetype.appliances.schedules
    usage.appliances = _appliances
    _control = ThermalControl()
    _control.cooling_set_point_schedules = archetype.thermal_control.cooling_set_point_schedules
    _control.heating_set_point_schedules = archetype.thermal_control.heating_set_point_schedules
    _control.hvac_availability_schedules = archetype.thermal_control.hvac_availability_schedules
    usage.thermal_control = _control
    _domestic_hot_water = DomesticHotWater()
    _domestic_hot_water.peak_flow = archetype.domestic_hot_water.peak_flow
    _domestic_hot_water.service_temperature = archetype.domestic_hot_water.service_temperature
    density = None
    if len(cold_water_temperature) > 0:
      cold_temperature = cold_water_temperature[cte.YEAR]['epw']
      density = archetype.domestic_hot_water.peak_flow * cte.WATER_DENSITY * cte.WATER_HEAT_CAPACITY \
                                    * (archetype.domestic_hot_water.service_temperature - cold_temperature)
    _domestic_hot_water.density = density
    _domestic_hot_water.schedules = archetype.domestic_hot_water.schedules
    usage.domestic_hot_water = _domestic_hot_water

  @staticmethod
  def _assign_comnet_extra_values(usage, archetype, occupancy_density):
    _occupancy = usage.occupancy
    archetype_density = archetype.occupancy.occupancy_density
    _occupancy.sensible_radiative_internal_gain = archetype.occupancy.sensible_radiative_internal_gain \
                                                  * occupancy_density / archetype_density
    _occupancy.latent_internal_gain = archetype.occupancy.latent_internal_gain * occupancy_density / archetype_density
    _occupancy.sensible_convective_internal_gain = archetype.occupancy.sensible_convective_internal_gain \
                                                   * occupancy_density / archetype_density

  @staticmethod
  def _calculate_reduced_values_from_extended_library(usage, archetype):
    number_of_days_per_type = {'WD': 251, 'Sat': 52, 'Sun': 62}
    total = 0
    for schedule in archetype.thermal_control.hvac_availability_schedules:
      if schedule.day_types[0] == cte.SATURDAY:
        for value in schedule.values:
          total += value * number_of_days_per_type['Sat']
      elif schedule.day_types[0] == cte.SUNDAY:
        for value in schedule.values:
          total += value * number_of_days_per_type['Sun']
      else:
        for value in schedule.values:
          total += value * number_of_days_per_type['WD']

    usage.hours_day = total / 365
    usage.days_year = 365

    max_heating_setpoint = cte.MIN_FLOAT
    min_heating_setpoint = cte.MAX_FLOAT

    for schedule in archetype.thermal_control.heating_set_point_schedules:
      if schedule.values is None:
        max_heating_setpoint = None
        min_heating_setpoint = None
        break
      if max(schedule.values) > max_heating_setpoint:
        max_heating_setpoint = max(schedule.values)
      if min(schedule.values) < min_heating_setpoint:
        min_heating_setpoint = min(schedule.values)

    min_cooling_setpoint = cte.MAX_FLOAT
    for schedule in archetype.thermal_control.cooling_set_point_schedules:
      if schedule.values is None:
        min_cooling_setpoint = None
        break
      if min(schedule.values) < min_cooling_setpoint:
        min_cooling_setpoint = min(schedule.values)

    usage.thermal_control.mean_heating_set_point = max_heating_setpoint
    usage.thermal_control.heating_set_back = min_heating_setpoint
    usage.thermal_control.mean_cooling_set_point = min_cooling_setpoint
