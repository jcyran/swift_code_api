from django.core.management.base import BaseCommand
from api.models import Country, BankBranch
import csv

class Command(BaseCommand):
    help = 'import bank branches from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='') as file:
            reader = csv.DictReader(file)

            for row in reader:
                country, created = Country.objects.get_or_create(
                    ISO2=row['COUNTRY ISO2 CODE'].upper(),
                    defaults={ 'country_name': row['COUNTRY NAME'].upper() },
                )

                BankBranch.objects.update_or_create(
                    swift_code=row['SWIFT CODE'],
                    defaults={
                        'bank_name': row['NAME'],
                        'bank_address': row['ADDRESS'],
                        'country': country,
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported branches.'))
