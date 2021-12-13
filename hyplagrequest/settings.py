import os
import logging

from pathlib import Path
from dotenv import load_dotenv
from os import environ

from .jwt_token import JwtToken

class HyplagConfig:

  class SingletonHelper(object):
    """The singleton-helper-class"""

    def __call__(self, *args, **kw):
      if HyplagConfig.instance is None:
        HyplagConfig.instance = HyplagConfig()

        return HyplagConfig.instance

  get_instance = SingletonHelper()
  instance = None

  # constants
  REQUIRED_ENV_VARS = {"HOST", "USERNAME", "PASSWORD"}

  # members
  config = None
  logger = None
  token = None
  scopes = '0'
  external_id = 'request'

  def __init__(self):
    """
    The constructor
    (keep in mind: this is a singleton, so just called once)
    """

    if HyplagConfig.instance is not None:
      raise RuntimeError('Multiple instances of singleton-class')

  def setup(self, credentials=None):
    """
    Setup the actual class.
    :param str filepath: path to the config-file (including file-name)
    """
    if self.logger is not None:
      self.logger.warning("Disallowed multiple setup of config.")
      return

    self.logger = logging.getLogger(__name__)
    if credentials is not None:
      self.load_config_from_dict(credentials)
    else:
      self.load_environment_variables()
      self.load_config_from_environ()
    self.get_token()

  def load_environment_variables(self):
    """
    Load .env file. Note the location is specified here and is assumed to be in the parent directory of module.
    """
    parent_path = Path(__file__)
    env_path = parent_path.parents[1] / '.env'
    self.logger.info("Loading file %s to read hyplag configuration parameters", env_path.resolve())
    load_dotenv(dotenv_path=env_path)

  def load_config_from_dict(self, credentials):
    """
    Loads the config-file
    """
    self.config = {}
    self.config['host'] = credentials['host']
    self.config['user'] = credentials['user']
    self.config['password'] = credentials['password']
    self.logger.info("Successfully loaded and stored environemnt parameters.")

  def load_config_from_environ(self):
    """
    Loads the config-file
    """
    self.config = {}
    self.config['host'] = os.getenv('HOST')
    self.config['user'] = os.getenv('USERNAME')
    self.config['password'] = os.getenv('PASSWORD')
    self.logger.info("Successfully loaded and stored environemnt parameters.")

  def enforce_environment_vars_complete(self):
    """
    Raises an exception if not all required environment variables are set
    """
    diff = self.REQUIRED_ENV_VARS.difference(environ)
    if len(diff) > 0:
      raise EnvironmentError(f'Failed because {diff} are not set')

  def get_token(self):
    self.token = JwtToken(self.config['host'], self.config['user'], self.config['password'])
