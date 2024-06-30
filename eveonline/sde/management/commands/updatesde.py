from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update static data"

    def add_arguments(self, parser):
        parser.add_argument("-d", "--debug", action="store_true", help="Use debug cache")
        parser.add_argument("-f", "--force", action="store_true", help="Do not use debug cache")

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Updating static data"))
