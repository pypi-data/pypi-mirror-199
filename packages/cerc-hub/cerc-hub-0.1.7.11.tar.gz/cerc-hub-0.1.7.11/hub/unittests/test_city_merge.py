"""
TestCityMerge test and validate the merge of several cities into one
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""
from pathlib import Path
from unittest import TestCase
from hub.imports.geometry_factory import GeometryFactory
import platform
from hub.exports.exports_factory import ExportsFactory
import subprocess
from subprocess import SubprocessError, TimeoutExpired, CalledProcessError
from hub.imports.results_factory import ResultFactory


class TestCityMerge(TestCase):
  """
  Functional TestCityMerge
  """
  def setUp(self) -> None:
    """
    Test setup
    :return: None
    """
    self._example_path = (Path(__file__).parent / 'tests_data').resolve()
    self._output_path = (Path(__file__).parent / 'tests_outputs').resolve()
    self._weather_file = (self._example_path / 'CAN_PQ_Montreal.Intl.AP.716270_CWEC.epw').resolve()
    self._climate_file = (self._example_path / 'New_York.cli').resolve()
    self._executable = None
    if platform.system() == 'Linux':
      self._executable = 'citysim_sra'
    if platform.system() == 'Darwin':
      self._executable = 'citysim_sra'
    elif platform.system() == 'Windows':
      self._executable = 'shortwave_integer'

  def _get_citygml(self, file):
    file_path = (self._example_path / file).resolve()
    city = GeometryFactory('citygml', path=file_path).city
    self.assertIsNotNone(city, 'city is none')
    return city

  def test_merge(self):
    city_1 = self._get_citygml('one_building_in_kelowna.gml')
    city_2 = self._get_citygml('pluto_building.gml')
    city = city_1.merge(city_2)
    self.assertEqual(len(city_1.city_objects), 1, 'Wrong amount of city_objects found in city_1')
    self.assertEqual(len(city_2.city_objects), 1, 'Wrong amount of city_objects found in city_2')
    self.assertEqual(len(city.city_objects), 2, 'Wrong amount of city_objects found in city')

  def test_merge_with_radiation(self):
    city_one = self._get_citygml('one_building_in_kelowna.gml')
    city_two = self._get_citygml('pluto_building.gml')
    city_two.name = 'New_York'
    city_two.climate_file = self._climate_file
    try:
      ExportsFactory(export_type='sra', city=city_two, path=self._output_path, weather_file=self._weather_file,
                     target_buildings=city_two.buildings, weather_format='epw').export()
      subprocess.run([self._executable, f'{str(self._output_path)}/{city_two.name}_sra.xml'], stdout=subprocess.DEVNULL)
    except (SubprocessError, TimeoutExpired, CalledProcessError) as error:
      raise Exception(error)
    ResultFactory('sra', city_two, self._output_path).enrich()
    merged_city = city_one.merge(city_two)
    self.assertEqual(len(merged_city.buildings), 2)
    self.assertEqual(round(merged_city.buildings[1].surfaces[0].global_irradiance['year'].iloc[0]), 254)
    self.assertEqual(merged_city.buildings[0].surfaces[0].global_irradiance, {})
    self.assertEqual(merged_city.buildings[0].surfaces[2].global_irradiance, {})
    self.assertEqual(city_one.buildings[0].surfaces[0].global_irradiance, merged_city.buildings[0].surfaces[0].global_irradiance)
    self.assertEqual(city_two.buildings[0].surfaces[0].global_irradiance, merged_city.buildings[1].surfaces[0].global_irradiance)
