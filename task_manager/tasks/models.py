from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label


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
    labels = models.ManyToManyField(Label,
                                    verbose_name=_('Labels'),
                                    blank=True)

    def __str__(self):
        return self.name
