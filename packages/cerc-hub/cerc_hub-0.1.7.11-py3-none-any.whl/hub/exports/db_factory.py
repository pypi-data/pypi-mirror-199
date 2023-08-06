"""
DBFactory performs read related operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project CoderPeter Yefi peteryefi@gmail.com
"""
import json
from typing import Union, Dict

from hub.persistence import City
from hub.persistence import Application
from hub.persistence import User
from hub.persistence import CityObject
from hub.persistence import SimulationResults


class DBFactory:
  """
  DBFactory class
  """

  def __init__(self, db_name, app_env, dotenv_path):
    self._city = City(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._application = Application(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._user = User(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._city_object = CityObject(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._simulation_results = SimulationResults(db_name=db_name, dotenv_path=dotenv_path, app_env=app_env)

  def application_info(self, application_uuid) -> Union[Application, None]:
    """
    Retrieve the application info for the given uuid
    :param application_uuid: the uuid for the application
    :return: Application or None
    """
    return self._application.get_by_uuid(application_uuid)

  def user_info(self, name, password, application_id):
    """
    Retrieve the user info for the given name and password and application_id
    :param name: the user name
    :param password: the user password
    :param application_id: the application id
    :return: User or None
    """
    return self._user.get_by_name_application_id_and_password(name, password, application_id)

  def user_login(self, name, password, application_uuid):
    """
    Retrieve the user info
    :param name: the user name
    :param password: the user password
    :param application_uuid: the application uuid
    :return: User or None
    """
    return self._user.get_by_name_application_uuid_and_password(name, password, application_uuid)

  def cities_by_user_and_application(self, user_id, application_id) -> [City]:
    """
    Retrieve the cities belonging to the user and the application
    :param user_id: User id
    :param application_id: Application id
    :return: [City]
    """
    return self._city.get_by_user_id_and_application_id(user_id, application_id)

  def building_info(self, name, city_id) -> Union[CityObject, None]:
    """
    Retrieve the building info
    :param name: Building name
    :param city_id: City Id
    :return: CityObject or None
    """
    return self._city_object.get_by_name_and_city(name, city_id)

  def results(self, user_id, application_id, cities, result_names=None) -> Dict:
    """
    Retrieve the simulation results for the given cities
    :param user_id: the user id owning the results
    :param application_id: the application id owning the results
    :param cities: dictionary containing the city and building names for the results
    :param result_names: if given, filter the results to the selected names
    """
    if result_names is None:
      result_names = []
    results = {}
    for city in cities['cities']:
      city_name = next(iter(city))
      result_set = self._city.get_by_user_id_application_id_and_name(user_id, application_id, city_name)
      if result_set is None:
        continue
      city_id = result_set.id
      results[city_name] = []
      for building_name in city[city_name]:
        if self._city_object.get_by_name_and_city(building_name, city_id) is None:
          continue
        city_object_id = self._city_object.get_by_name_and_city(building_name, city_id).id
        _ = self._simulation_results.get_simulation_results_by_city_id_city_object_id_and_names(
          city_id,
          city_object_id,
          result_names)

        for value in _:
          values = json.loads(value.values)
          values["building"] = building_name
          results[city_name].append(values)
    return results
