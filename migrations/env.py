from __future__ import with_statement
import logging
from logging.config import fileConfig
from flask import current_app
from alembic import context
from alembic import command
from alembic.config import Config
from alembic.runtime.environment import EnvironmentContext

# Instantiate a Config object by passing the name of your .ini file
config = Config('alembic.ini')# Instantiate an EnvironmentContext object

# Instantiate an EnvironmentContext object
env_context = EnvironmentContext(config, None)

# Use the env_context to access the config object
config_object = env_context.config


# Now you can use the config object to access Alembic configuration options
some_param = config_object.get_main_option("my option")


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = config_object

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option(
    'sqlalchemy.url',
    str(current_app.extensions['migrate'].db.get_engine().url).replace(
        '%', '%%'))
target_metadata = current_app.extensions['migrate'].db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    command.upgrade(config, "head")

def run_migrations_online():
    command.upgrade(config, "head")

if __name__ == "__main__":
    is_offline = True  # Set this to True or False based on your needs

    if is_offline:
        run_migrations_offline()
    else:
        run_migrations_online()