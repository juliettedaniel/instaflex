from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic.config import Config
from alembic import command
from alembic.runtime.migration import MigrationContext
from alembic.runtime.environment import EnvironmentContext
from sqlalchemy import MetaData


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = Config("InstaFlex/alembic.ini")

# Create a connection engine from the config options
engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix='sqlalchemy.',
    poolclass=pool.NullPool
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# This line configures the migration context with the connection engine
migration_ctx = MigrationContext.configure(engine)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    command.upgrade(config, "head")

def run_migrations_online():
    target_metadata = MetaData()  # Declare and assign target_metadata outside of the if condition
    with engine.connect() as connection:
        current_command = command.current(config)
        if current_command == "upgrade":
            with EnvironmentContext(config, migration_ctx):  # Remove the fn parameter from EnvironmentContext
                migration_ctx.configure(
                    connection=connection
                )
                with migration_ctx.begin_transaction():
                    target_metadata.reflect(bind=connection)
                    migration_ctx.run_migrations()
        else:
            # Handle other commands here
            pass

run_migrations_online()

