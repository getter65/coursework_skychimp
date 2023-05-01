from django.core.management import BaseCommand
from django.core import management


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("args", metavar="payment", nargs="+", help="")

    def handle(self, *args, **options):
        file = args[0]
        print(f'loading data to payments from {file}')
        management.call_command('loaddata', file, verbosity=0)
