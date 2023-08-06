"""
User performs user related crud operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project CoderPeter Yefi peteryefi@gmail.com
"""
from hub.persistence import User


class UserFactory:
  """
  UserFactory class
  """

  def __init__(self, db_name, app_env, dotenv_path):
    self._user_repo = User(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)

  def login_user(self, name: str,  password: str, application_id: int):
    """
    Retrieve a single city from postgres
    :param name: the email of the user
    :param password: the password of the user
    :param application_id: the id of the application accessing hub
    """
    return self._user_repo.get_by_name_application_and_password(name, password, application_id)

  def get_by_name_and_application(self, name: str, application: int):
    """
    Retrieve a single user
    :param name: user name
    :param application: application accessing hub
    """
    return self._user_repo.get_by_name_and_application(name, application)
