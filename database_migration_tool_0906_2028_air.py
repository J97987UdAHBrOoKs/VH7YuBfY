# 代码生成时间: 2025-09-06 20:28:40
import cherrypy
import logging
from cherrypy.lib import cptools
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from contextlib import closing

# Configuration
DATABASE_URI = 'postgresql://username:password@localhost:5432/dbname'
MIGRATION_SCRIPTS = [
    ('001_initial_migration.sql', '001_rollback.sql'),
    ('002_add_users_table.sql', '002_rollback.sql'),
    # Add more migration scripts here
]

class MigrationException(Exception):
    pass

class DatabaseMigrationBuilder:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)

    def run_migration(self, script):
        """Execute a single migration script."""
        with closing(self.engine.connect()) as connection:
            with connection.begin():
                with open(script, 'r') as file:
                    connection.execute(file.read())

    def rollback_migration(self, script):
        """Execute a single rollback script."""
        with closing(self.engine.connect()) as connection:
            with connection.begin():
                with open(script, 'r') as file:
                    connection.execute(file.read())

    def migrate(self):
        """Apply all migration scripts."""
        for migration, _ in MIGRATION_SCRIPTS:
            try:
                self.run_migration(migration)
            except SQLAlchemyError as e:
                logging.error(f'Migration failed: {e}')
                raise MigrationException(f'Migration {migration} failed.')

    def rollback(self):
        """Rollback all migration scripts."""
        for _, rollback in reversed(MIGRATION_SCRIPTS):
            try:
                self.rollback_migration(rollback)
            except SQLAlchemyError as e:
                logging.error(f'Rollback failed: {e}')
                raise MigrationException(f'Rollback {rollback} failed.')

class MigrationWebService:
    @cherrypy.expose
    @cptools.json_out()
    def migrate(self):
        """REST endpoint to run database migrations."" "
        try:
            builder = DatabaseMigrationBuilder()
            builder.migrate()
            return {'status': 'success', 'message': 'Migration completed successfully.'}
        except MigrationException as e:
            return {'status': 'error', 'message': str(e)}

    @cherrypy.expose
    @cptools.json_out()
    def rollback(self):
        """REST endpoint to rollback database migrations."" "
        try:
            builder = DatabaseMigrationBuilder()
            builder.rollback()
            return {'status': 'success', 'message': 'Rollback completed successfully.'}
        except MigrationException as e:
            return {'status': 'error', 'message': str(e)}

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    cherrypy.config.update({'server.socket_port': 8080})
    cherrypy.quickstart(MigrationWebService())