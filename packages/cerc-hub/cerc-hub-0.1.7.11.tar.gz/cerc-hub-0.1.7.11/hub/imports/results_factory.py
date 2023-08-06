"""
Result factory retrieve the specific tool results and store the data in the given city
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""
from pathlib import Path

from hub.helpers.utils import validate_import_export_type
from hub.hub_logger import logger
from hub.imports.results.simplified_radiosity_algorithm import SimplifiedRadiosityAlgorithm
from hub.imports.results.insel_monthly_energry_balance import InselMonthlyEnergyBalance
from hub.imports.results.insel_heatpump_energy_demand import InselHeatPumpEnergyDemand


class ResultFactory:
  """
  ResultFactory class
  """

  def __init__(self, handler, city, base_path=None, hp_model=None):
    """

    :param handler: pointer to results class to be called
    :param city: the city object
    :param base_path: the path to result output file
    :param hp_model: (optional) the heat pump model for which
    results are being retrieved
    """
    if base_path is None:
      base_path = Path(Path(__file__).parent.parent / 'data/results')
    self._handler = '_' + handler.lower().replace(' ', '_')
    class_funcs = validate_import_export_type(ResultFactory)
    if self._handler not in class_funcs:
      err_msg = f"Wrong import type [{self._handler}]. Valid functions include {class_funcs}"
      logger.error(err_msg)
      raise Exception(err_msg)
    self._city = city
    self._base_path = base_path
    self._hp_model = hp_model

  def _sra(self):
    """
    Enrich the city with Simplified Radiosity Algorithm results
    """
    SimplifiedRadiosityAlgorithm(self._city, self._base_path).enrich()

  def _heat_pump(self):
    """
    Enrich the city (energy system specifically) with heat pump insel simulation
    results
    """
    InselHeatPumpEnergyDemand(self._city, self._base_path, self._hp_model).enrich()

  def _insel_meb(self):
    """
    Enrich the city with insel monthly energy balance results
    """
    InselMonthlyEnergyBalance(self._city, self._base_path).enrich()

  def enrich(self):
    """
    Enrich the city given to the class using the usage factory given handler
    :return: None
    """
    getattr(self, self._handler, lambda: None)()
