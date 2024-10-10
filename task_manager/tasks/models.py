from django.db import models
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


class Task(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'), unique=True)
    description = models.TextField(verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey('statuses.Status',
                               on_delete=models.PROTECT,
                               verbose_name=_('Status'))
    author = models.ForeignKey('auth.User',
                               on_delete=models.PROTECT,
                               verbose_name=_('Author'),
                               related_name='author')
    executor = models.ForeignKey('auth.User',
                                 on_delete=models.PROTECT,
                                 verbose_name=_('Executor'),
                                 related_name='executor',
                                 null=True,
                                 blank=True)
    # todo переопределить поле метка
    labels = models.ManyToManyField('self',
                                    verbose_name=_('Labels'),
                                    blank=True, )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if Task.objects.filter(status=self.pk).exists():
            raise ProtectedError("Cannot delete status because it is in use",
                                 Task.objects.filter(status=self.pk))

        super().delete(*args, **kwargs)
