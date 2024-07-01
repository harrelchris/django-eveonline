from django.db import models


class Hash(models.Model):
    value = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.date.isoformat()

    def is_current(self, remote_hash: str) -> bool:
        return self.value == remote_hash

    def update_hash(self, remote_hash: str):
        self.value = remote_hash
        self.save()


class Categories(models.Model):
    name = models.CharField(max_length=256)


class ContrabandTypes(models.Model):
    faction_id = models.IntegerField()
    type_id = models.IntegerField()
    standing_loss = models.FloatField()
    confiscate_min_sec = models.FloatField()
    fine_by_value = models.FloatField()
    attack_min_sec = models.FloatField()


class ControlTowerResources(models.Model):
    control_tower_type_id = models.IntegerField()  # TODO: should be id?
    resource_type_id = models.IntegerField()
    purpose = models.IntegerField()
    quantity = models.IntegerField()
    min_security_level = models.IntegerField()
    faction_id = models.IntegerField()


class Flags(models.Model):
    name = models.CharField(max_length=256)
    text = models.CharField(max_length=256)
    order_id = models.IntegerField()


class Groups(models.Model):
    pass


class Items(models.Model):
    pass


class MarketGroups(models.Model):
    pass


class MetaGroups(models.Model):
    pass


class MetaTypes(models.Model):
    pass


class Names(models.Model):
    pass


class Positions(models.Model):
    pass


class Traits(models.Model):
    pass


class TypeMaterials(models.Model):
    pass


class Types(models.Model):
    pass


class UniqueNames(models.Model):
    pass


class Volumes(models.Model):
    pass
