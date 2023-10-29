from django.db import models
from django.conf import settings


class Gym(models.Model):
    '''Model for gym details.'''
    name = models.CharField(max_length=255, unique=True, verbose_name='نام')
    number = models.CharField(max_length=255, unique=True, verbose_name='شماره تلفن')
    address = models.CharField(max_length=255, verbose_name='آدرس')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='مالک'
        )
    days_closed = models.CharField(max_length=255, verbose_name='روزهای تعطیل')
    hour_open = models.TimeField(verbose_name='ساعت شروع')
    hour_close = models.TimeField(verbose_name='ساعت بستن')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'سالن ورزش'
        verbose_name_plural = 'سالن ورزش'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='نویسنده'
    )
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='review', verbose_name='باشگاه'
        )
    name = models.CharField(max_length=255, verbose_name='نام')
    description = models.TextField(verbose_name='توضیحات')

    class Meta:
        verbose_name = 'دیدگاه'
        verbose_name_plural = 'دیدگاه ها'

    def __str__(self):
        return str(self.author)


class Social(models.Model):
    gym = models.ForeignKey(
        Gym,
        on_delete=models.CASCADE,
        related_name='social',
        verbose_name='باشگاه'
        )
    name = models.CharField(max_length=255, verbose_name='نام')
    link = models.CharField(max_length=255, verbose_name='لینک')

    class Meta:
        verbose_name = 'رسانه اجتماعی'
        verbose_name_plural = 'رسنه های اجتماعی'

    def __str__(self):
        return self.name
