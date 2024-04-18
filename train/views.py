from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import TrainSerializer
from .models import Train, Seat
from redis_client import redis_client, LOCK_EXPIRATION_TIME

# Create your views here.

class AddTrain(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
            if not request.user.is_staff:
                return Response({"error": "You are not authorized to add train"}, status=403)
            serializers = TrainSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response({"message": "Train added successfully"})
            else:
                return Response(serializers.errors)
            
class GetTrainAvailability(APIView):
    def get(self, request):
        data = request.data
        if "source" not in data or "destination" not in data:
            return Response({"error": "Source and destination are required"}, status=400)
        source = data["source"]
        destination = data["destination"]
        trains = Train.objects.filter(source=source, destination=destination)
        if not trains:
            return Response({"message": "No trains available"})
        response = []
        for train in trains:
            # check for the available seats and if the seat is locked dont show it
            seats = Seat.objects.filter(train=train, is_booked=False)
            available_seats = []
            for seat in seats:
                key = f"seat:{seat.id}"
                
                if redis_client.exists(key):
                    continue
                available_seats.append(seat.seat_number)

            response.append({
                "train_id": train.id,
                "train_name": train.train_name,
                "train_capacity": train.train_capacity,
                "remaining_capacity": train.remaining_capacity(),
                "is_full": train.is_full(),
                "source": train.source,
                "destination": train.destination,
                "seat_available": available_seats
            })
        return Response(response)
    
class ViewBookings(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        seats = Seat.objects.filter(user=user)
        if not seats:
            return Response({"message": "No bookings found"})
        response = []
        for seat in seats:
            response.append({
                "train_id": seat.train.id,
                "train_name": seat.train.train_name,
                "seat_number": seat.seat_number,
                "source": seat.train.source,
                "destination": seat.train.destination,
            })
        return Response(response)
    
def lock_seat(seat_id) -> None:
    key = f"seat:{seat_id}"
    acquired = redis_client.set(key, "locked", ex=LOCK_EXPIRATION_TIME, nx=True)
    if not acquired:
        raise Exception("Seat is already locked")
    
def unlock_seat(seat_id) -> None:
    key = f"seat:{seat_id}"
    redis_client.delete(key)

class BookTrain(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        if "train_id" not in data or "seat_number" not in data:
            return Response({"error": "train_id and seat_number are required"}, status=400)
        train_id = data["train_id"]
        seat_number = data["seat_number"]
        try:
            seat = Seat.objects.get(train_id=train_id, seat_number=seat_number)
        except Seat.DoesNotExist:
            return Response({"error": "Invalid train_id or seat_number"}, status=400)
        if seat.is_booked:
            return Response({"error": "Seat is already booked"}, status=400)
        try:
            lock_key = f"seat:{seat.id}"
            print(lock_key)
            if redis_client.exists(lock_key):
                return Response({"error": "Seat is already locked"}, status=400)
            lock_seat(seat.id)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        
        return Response({"seat_id": seat.id, "message": "Seat locked successfully. Confirm booking to book the seat"})
        
class confirmBooking(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        data = request.data
        if "seat_id" not in data:
            return Response({"error": "seat_id is required"}, status=400)
        seat_id = data["seat_id"]
        try:
            if not redis_client.exists(f"seat:{seat_id}"):
                return Response({"error": "Seat is not locked"}, status=400)
            seat = Seat.objects.get(id=seat_id)
            seat.is_booked = True
            seat.user = user
            seat.save()
            unlock_seat(seat_id)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        return Response({"message": "Seat booked successfully"})
    

        


        
    

        

    

    

            

            
        

        


