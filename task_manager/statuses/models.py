from django.db import models
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task_set = None

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.task_set and self.task_set.exists():
            raise ProtectedError("Cannot delete status because it is in use",
                                 self.task_set.all())

        super().delete(*args, **kwargs)