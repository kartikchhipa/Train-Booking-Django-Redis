from django.urls import path
from .views import AddTrain, GetTrainAvailability, BookTrain, confirmBooking, ViewBookings

urlpatterns = [
    path('add-train/', AddTrain.as_view(), name='add-train'),
    path('get-train/', GetTrainAvailability.as_view(), name='get-train-availability'),
    path('book-train/', BookTrain.as_view(), name='book-train'),
    path('confirm-booking/', confirmBooking.as_view(), name='confirm-booking'),
    path('view-bookings/', ViewBookings.as_view(), name='view-booking')

]