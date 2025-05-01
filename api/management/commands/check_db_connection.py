from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time

class Command(BaseCommand):
    help = 'Wait for database to be ready'

    def add_arguments(self, parser):
        parser.add_argument('--retry', type=int, default=30, help='Number of retries')

    def handle(self, *args, **options):
        max_retries = options['retry']
        retry_count = 0
        
        self.stdout.write("Waiting for database...")
        db_conn = None
        
        while retry_count < max_retries:
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS('Database is available!'))
                return
            except OperationalError:
                retry_count += 1
                self.stdout.write(f"Database unavailable, waiting 1 second (retry {retry_count}/{max_retries})...")
                time.sleep(1)
        
        self.stdout.write(self.style.ERROR('Max retries reached. Database still not available.'))
        raise OperationalError("Could not connect to database")
