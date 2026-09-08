from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', default=False)
        # accepted for compatibility with juntagrico's built-in list generation
        # UI, but not applicable to custom-sub depot lists
        parser.add_argument('--future', action='store_true', default=False)
        parser.add_argument('--no-future', dest='no_future', action='store_true', default=False)
        parser.add_argument('--days', type=int, default=0)

    def handle(self, *args, **options):
        call_command('cs_generate_depot_list', force=options['force'])
