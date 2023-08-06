"""
Test EnergySystemsFactory and various heatpump models
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import unittest
from unittest import TestCase

import sqlalchemy.exc

from hub.imports.geometry_factory import GeometryFactory
from hub.imports.db_factory import DBFactory
from hub.imports.user_factory import UserFactory
from hub.exports.db_factory import DBFactory as ExportDBFactory
from hub.persistence.repository import Repository
from sqlalchemy import create_engine
from hub.persistence.models import City, Application, CityObject
from hub.persistence.models import User, UserRoles
from sqlalchemy.exc import ProgrammingError
import uuid

class Skip:

  _value = False
  _message = 'PostgreSQL not properly installed in host machine'

  def __init__(self):
    # Create test database
    env = '/usr/local/etc/hub/.env'
    repo = Repository(db_name='test_db', app_env='TEST', dotenv_path=env)
    eng = create_engine(f'postgresql://{repo.configuration.get_db_user()}@/{repo.configuration.get_db_user()}')
    try:
      # delete test database if it exists
      conn = eng.connect()
      conn.execute('commit')
      conn.execute('DROP DATABASE test_db')
      conn.close()
    except ProgrammingError as err:
      print(f'Database does not exist. Nothing to delete')
    except sqlalchemy.exc.OperationalError:
      self._value = True

  @property
  def value(self):
    return  self._value

  @property
  def message(self):
    return self._message

  @value.setter
  def value(self, skip_value):
    self._value = skip_value

skip = Skip()

class TestDBFactory(TestCase):
  """
  TestDBFactory
  """

  @classmethod
  def setUpClass(cls) -> None:
    """
    Test setup
    :return: None
    """
    # Create test database
    env = '/usr/local/etc/hub/.env'
    repo = Repository(db_name='test_db', app_env='TEST', dotenv_path=env)
    eng = create_engine(f'postgresql://{repo.configuration.get_db_user()}@/{repo.configuration.get_db_user()}')
    try:
      # delete test database if it exists
      conn = eng.connect()
      conn.execute('commit')
      conn.execute('DROP DATABASE test_db')
      conn.close()
    except ProgrammingError as err:
      print(f'Database does not exist. Nothing to delete')
    except sqlalchemy.exc.OperationalError:
      skip.value = True
      return
    cnn = eng.connect()
    cnn.execute('commit')
    cnn.execute("CREATE DATABASE test_db")
    cnn.close()

    Application.__table__.create(bind=repo.engine, checkfirst=True)
    User.__table__.create(bind=repo.engine, checkfirst=True)
    City.__table__.create(bind=repo.engine, checkfirst=True)
    CityObject.__table__.create(bind=repo.engine, checkfirst=True)

    city_file = "tests_data/C40_Final.gml"
    cls.city = GeometryFactory('citygml', city_file).city
    cls._db_factory = DBFactory(db_name='test_db', app_env='TEST', dotenv_path=env)
    cls._export_db_factory = ExportDBFactory(db_name='test_db', app_env='TEST', dotenv_path=env)
    user_factory = UserFactory(db_name='test_db', app_env='TEST', dotenv_path=env)
    cls.unique_id = str(uuid.uuid4())
    cls.application = cls._db_factory.persist_application("test", "test application", cls.unique_id)
    cls._user = user_factory.create_user("Admin", cls.application.id, "Admin@123", UserRoles.Admin)
    cls.pickle_path = 'tests_data/pickle_path.bz2'

  @unittest.skipIf(skip.value, skip.message)
  def test_save_application(self):
    self.assertEqual(self.application.name, "test")
    self.assertEqual(self.application.description, "test application")
    self.assertEqual(str(self.application.application_uuid), self.unique_id)

  @unittest.skipIf(skip.value, skip.message)
  def test_save_city(self):
    self.city.name = "Montréal"
    saved_city = self._db_factory.persist_city(self.city, self.pickle_path, self.application.id, self._user.id)
    self.assertEqual(saved_city.name, 'Montréal')
    self.assertEqual(saved_city.pickle_path, self.pickle_path)
    self.assertEqual(saved_city.level_of_detail, self.city.level_of_detail.geometry)
    self._db_factory.delete_city(saved_city.id)

  @unittest.skipIf(skip.value, skip.message)
  def test_get_city_by_name(self):
    city = self._db_factory.persist_city(self.city, self.pickle_path, self.application.id, self._user.id)
    retrieved_city = self._export_db_factory.get_city_by_name(city.name)
    self.assertEqual(retrieved_city[0].application_id, 1)
    self.assertEqual(retrieved_city[0].user_id, self._user.id)
    self._db_factory.delete_city(city.id)

  @unittest.skipIf(skip.value, skip.message)
  def test_get_city_by_user(self):
    city = self._db_factory.persist_city(self.city, self.pickle_path, self.application.id, self._user.id)
    retrieved_city = self._export_db_factory.get_city_by_user(self._user.id)
    self.assertEqual(retrieved_city[0].pickle_path, self.pickle_path)
    self._db_factory.delete_city(city.id)

  @unittest.skipIf(skip.value, skip.message)
  def test_get_city_by_id(self):
    city = self._db_factory.persist_city(self.city, self.pickle_path, self.application.id, self._user.id)
    retrieved_city = self._export_db_factory.get_city(city.id)
    self.assertEqual(retrieved_city.level_of_detail, self.city.level_of_detail.geometry)
    self._db_factory.delete_city(city.id)

  @unittest.skipIf(skip.value, skip.message)
  def test_get_update_city(self):
    city = self._db_factory.persist_city(self.city, self.pickle_path, self.application.id, self._user.id)
    self.city.name = "Ottawa"
    self._db_factory.update_city(city.id, self.city)
    updated_city = self._export_db_factory.get_city(city.id)
    self.assertEqual(updated_city.name, self.city.name)
    self._db_factory.delete_city(city.id)
