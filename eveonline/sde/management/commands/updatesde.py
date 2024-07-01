import sys

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db.transaction import atomic

from eveonline.sde import pipelines
from eveonline.sde import services
from eveonline.sde.models import Hash

PIPELINES = [
    pipelines.Categories(),
    pipelines.ContrabandTypes(),
    pipelines.ControlTowerResources(),
    pipelines.Flags(),
    pipelines.Groups(),
    pipelines.Items(),
    pipelines.MarketGroups(),
    pipelines.MetaGroups(),
    pipelines.MetaTypes(),
    pipelines.Names(),
    pipelines.Positions(),
    pipelines.Traits(),
    pipelines.TypeMaterials(),
    pipelines.Types(),
    pipelines.UniqueNames(),
    pipelines.Volumes(),
]


class Command(BaseCommand):
    help = "Update static data"

    def add_arguments(self, parser):
        parser.add_argument("-c", "--cache", action="store_true", help="Use cache even when not in debug mode")
        parser.add_argument("-n", "--no-cache", action="store_true", help="Do not use cache even when in debug mode")

    def handle(self, *args, **options):
        cache = self.get_cache(options)
        if not cache:
            self.stdout.write(self.style.SUCCESS("Checking for updates..."))
            local_hash, created = Hash.objects.get_or_create(id=1, defaults=dict(value=""))
            remote_hash = services.get_remote_hash()
            if local_hash.is_current(remote_hash=remote_hash):
                self.stdout.write(self.style.SUCCESS("Static data is current"))
                sys.exit(0)
            else:
                local_hash.update_hash(remote_hash=remote_hash)
                self.stdout.write(self.style.WARNING("Updating static data..."))

        services.disable_foreign_key_verification()
        with atomic():
            for pipeline in PIPELINES:
                pipeline.run(cache=cache)
        services.enable_foreign_key_verification()
        self.stdout.write(self.style.SUCCESS("Static data updated"))

    def get_cache(self, options) -> bool:
        if options["cache"] and options["no_cache"]:
            raise CommandError("--cache and --no-cache flags may not be used together")

        if options["cache"]:
            return True
        elif options["no_cache"]:
            return False
        else:
            return settings.DEBUG
