from django.db import models
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """
        Проверка на использование метки в задачах

        Возбуждает ProtectedError если метка используется хотя бы одной задачей
        """
        if self.task_set.exists():
            raise ProtectedError("Cannot delete label because it is in use",
                                 self.task_set.all())

        super().delete(*args, **kwargs)
