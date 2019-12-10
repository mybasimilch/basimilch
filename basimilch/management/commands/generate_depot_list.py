from django.core.management.base import BaseCommand
from django.core.management import call_command
import logging


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('cs_generate_depot_list')
        call_command('cs_generate_pack_list')
