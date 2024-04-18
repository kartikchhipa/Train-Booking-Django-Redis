from django.urls import path
from .views import AddTrain, GetTrainAvailability, BookTrain, confirmBooking

urlpatterns = [
    path('add-train/', AddTrain.as_view(), name='add-train'),
    path('get-train/', GetTrainAvailability.as_view(), name='get-train-availability'),
    path('book-train/', BookTrain.as_view(), name='book-train'),
    path('confirm-booking/', confirmBooking.as_view(), name='confirm-booking')

]