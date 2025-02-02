from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    origin = models.CharField(max_length=100)
    origin_location = models.CharField(max_length=100, blank=True)
    destination = models.CharField(max_length=100)
    destination_location = models.CharField(max_length=100, blank=True)
    need_pro_mover = models.BooleanField(default=False)
    need_box_packer = models.BooleanField(default=False)
    move_date = models.DateTimeField()
    items_detected = models.ManyToManyField('DetectedItem', blank=True, related_name='orders')  # افزودن related_name

class DetectedItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='detected_items')  # افزودن related_name
    item_class = models.CharField(max_length=50)
    confidence = models.FloatField()
    bbox = models.JSONField()

class Photo(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='photos/')

class Mover(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=100)
    MOVER_TYPES = [
        ('mover', 'Mover'),
        ('box_packer', 'Box Packer'),
        ('driver', 'Driver'),
        ('driver_no_cargo', 'Driver without Cargo'),
    ]
    mover_type = models.CharField(max_length=20, choices=MOVER_TYPES)
