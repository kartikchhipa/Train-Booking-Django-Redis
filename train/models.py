from django.db import models
import uuid
from user.models import User

# Create your models here.

from django.db.models.signals import post_save
from django.dispatch import receiver



class Train(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    train_name = models.CharField(max_length=255)
    train_capacity = models.IntegerField()    
    source = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    occupancy = models.IntegerField(default=0)

    def __str__(self):
        return self.train_name
    
    def remaining_capacity(self):
        return self.train_capacity - self.occupancy
    
    def is_full(self):
        return self.occupancy == self.train_capacity
    
@receiver(post_save, sender=Train)
def create_seats(sender, instance, created, **kwargs):
    if created:
        # Create seats for the train
        for seat_number in range(1, instance.train_capacity + 1):
            Seat.objects.create(train=instance, seat_number=seat_number)

class Seat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.id} - {self.train.train_name} - {self.seat_number}'
    

    

    


    

    

