from django.db import models


class Memory(models.Model):
    name = models.CharField(max_length=150)
    comment = models.TextField()

    user = models.ForeignKey(
        'auth.User',
        related_name='memories',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Memories'


    def __str__(self):
        return self.name
