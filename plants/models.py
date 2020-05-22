from django.conf import settings
from django.db import models



# Create your models here.
class UserMixin(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # zapewnia używanie obecnego modelu użytkownika
        on_delete=models.PROTECT,
        null=False, blank=False,
        verbose_name='User',
        help_text='',
    )

    class Meta: # żeby django nie stworzyło osobnej tabeli w bazie danych
        abstract = True


class Category(UserMixin, models.Model):
    name = models.CharField(
        max_length=50,
        null=False, blank=False,
        verbose_name='Name',
        help_text='',
    )

    slug = models.SlugField() # -> lukasz-zdzblo, często jako identyfikator

    description = models.CharField(
        max_length=150,
        null=False, blank=True, default='', # blank - opcja djangowa, np. w formularzu akceptuje puste pole
        verbose_name='Description',
        help_text='',
    )

    image_url = models.URLField(
        verbose_name='Image URL',
        help_text='',
    )


# ogólny rodzaj kwiatka
class Plant(UserMixin, models.Model):
    name = models.CharField(
        max_length=50,
        null=False, blank=False,
        verbose_name='Name',
        help_text='',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        null=False, blank=False,
        verbose_name='Category',
        help_text='',
    )

    watering_interval = model.PositiveIntegerField(
        null=False, blank=False,
        verbose_name='Watering interval',
        help_text='In seconds', # na potrzeby symulacji/testów w trakcie tworzenia aplikacji
    )

    fertilizing_interval = model.PositiveIntegerField(
        null=False, blank=False,
        verbose_name='Fertilizing interval',
        help_text='In seconds',
    )

    EXPOSURE_CHOICES = [
        ('dark','Dark'),
        ('shade','Shade'),
        ('partsun','Part sun'),
        ('fullsun','Full sun'),
    ]

    required_exposure = models.CharField(
        max_length=10, choices=EXPOSURE_CHOICES, # ograniczenie max 10 dotyczy tylko lewej strony tupli w EXPOSURE_CHOICES
        null=False, blank=False,
        verbose_name='Amount of sun',
        help_text='',
    )

    HUMIDITY_CHOICES = [
        ('low','Low'),
        ('medium','Medium'),
        ('high','High'),
    ]

    required_humidity = models.CharField(
        max_length=10, choices=HUMIDITY_CHOICES,
        null=False, blank=False,
        verbose_name='Humidity',
        help_text='',
    )

    TEMPERATURE_CHOICES = [
        ('cold','Cold'),
        ('medium','Medium'),
        ('warm','Warm'),
    ]

    required_temperature = models.CharField(
        max_length=10, choices=TEMPERATURE_CHOICES,
        null=False, blank=False,
        verbose_name='Temperature',
        help_text='',
    )

    blooming = models.BooleanField(
        default=False,
        null=False, blank=True, # np wymaganie akceptacji regulaminu strony, jeśli blank=False - user musi się zgodzić!
        verbose_name='Blooming',
        help_text='',
    )

    DIFFICULTY_CHOICES = [
        ('1','Low'),
        ('2','Medium-low'),
        ('3','Medium'),
        ('4','Medium-high'),
        ('5','High'),
    ]

    difficulty = models.PositiveIntegerField(
        choices=DIFFICULTY_CHOICES,
        null=False, blank=False, default=1,
        verbose_name='Cultivation difficulty level'
        help_text='',
    )


class Room(UserMixin, models.Model):
    name = models.CharField(
        max_length=50,
        null=False, blank=False,
        verbose_name='Room',
        help_text='',
    )

    EXPOSURE_CHOICES = [
        ('dark','Dark'),
        ('shade','Shade'),
        ('partsun','Part sun'),
        ('fullsun','Full sun'),
    ]

    room_exposure = models.CharField(
        max_length=10, choices=EXPOSURE_CHOICES,
        null=False, blank=False,
        verbose_name='Exposure',
        help_text='',
    )

    HUMIDITY_CHOICES = [
        ('low','Low'),
        ('medium','Medium'),
        ('high','High'),
    ]

    room_humidity = models.CharField(
        max_length=10, choices=HUMIDITY_CHOICES,
        null=False, blank=False,
        verbose_name='Humidity',
        help_text='',
    )

    TEMPERATURE_CHOICES = [
        ('cold','Cold'),
        ('medium','Medium'),
        ('warm','Warm'),
    ]

    room_temperature = models.CharField(
        max_length=10, choices=TEMPERATURE_CHOICES,
        null=False, blank=False,
        verbose_name='Temperature',
        help_text='',
    )

    drafty = models.BooleanField(
        default=False,
        null=False, blank=True,
        verbose_name='Drafty',
        help_text='',
    )


class UserPlant(UserMixin, models.Model):
    name = models.CharField(
        max_length=50,
        null=False, blank=False,
        verbose_name='Name',
        help_text='',
    )

    description = models.CharField(
        max_length=150,
        null=False, blank=True, default='',
        verbose_name='Description',
        help_text='',
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.PROTECT,
        null=False, blank=False,
        verbose_name='Room',
        help_text='',
    )

    watering_time = models.DateTimeField(
        verbose_name='Last watering time',
        help_text='',
    )

    fertilizing_time = models.DateTimeField(
        verbose_name='Last fertilizing time',
        help_text='',
    )
