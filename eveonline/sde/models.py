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
