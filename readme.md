# Train Booking Platform with Django And Redis
This is a simple train booking platform built with Django and Redis. The platform allows users to check the trains between source and destination, book a train ticket and view their booking history. 
- Used **Redis** as a caching Layer for concurrency control to store the seats locked by the user during the booking process. 
- Used **Django signals** (post save) to create the seats for the train when a new train is added to the system.  
- Used **JWT Authentication** for user authentication and authorization by creating access and refresh tokens to grant conditional access to some apis based on the user role.

## Instructions to run the project
1. Clone the repository using the following command
```bash 
git clone https://github.com/kartikchhipa/Train-Booking-Django-Redis.git
```
2. Change the directory to the project directory
```bash
cd Train-Booking-Django-Redis
```
3. Create a virtual environment using the following command
```bash
python3 -m venv env
```
4. Activate the virtual environment using the following command
```bash
source env/bin/activate
```
5. Install the dependencies using the following command
```bash
pip install -r requirements.txt
```
6. Run the following command to start the server
```bash
python manage.py runserver
```
7. To Create a superuser run the following command
```bash
python manage.py createsuperuser
```
8. Install Redis and start the Redis server
9. Check if the Redis server is running by running the following command
```bash
redis-cli ping
```


## APIs
1. **Register User**
   - **URL:** /user/register/
   - **Method:** POST
   - **Request Body:**
     ```json
     {
        "username": "testuser",
        "email": "test@test.com",
        "password": "testpassword",
        "password2": "testpassword"
     }
        ```
    - **Response:**
        ```json
        {
            "message": "User registered successfully"
        }
        ```
2. **Login User**
    - **URL:** /user/login/
    - **Method:** POST
    - **Request Body:**
      ```json
      {
          "username": "kartik",
          "password": "kc123123"
      }
      ```
     - **Response:**
          ```json
            {
                "token": {
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxMzU0NjcwMSwiaWF0IjoxNzEzNDYwMzAxLCJqdGkiOiJjYWViZTEzMTI2OGY0ODAxYjg2YzhiNmU5ODMzMGI3YyIsInVzZXJfaWQiOiJiMTZmYmM0YS1hZmEyLTRiZDYtOGUxYi05N2Y2ZjFmZTc5OTIifQ.v128NocN1JHxx0kCAOhGVTjgUFn5WdPsF_vAZ599aQ0",
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzEzNDYxNTAxLCJpYXQiOjE3MTM0NjAzMDEsImp0aSI6ImRiMDkzNjRjM2M5MTRiNGFiY2YzNTgyMjcxMjgyYzUwIiwidXNlcl9pZCI6ImIxNmZiYzRhLWFmYTItNGJkNi04ZTFiLTk3ZjZmMWZlNzk5MiJ9._CzGACDzQDdqc2y8CQ4C_qbtEqMGoHLCZeMafUY5d3A"
                },
                "msg": "Login successful"
            }
         ```
3. **Add Train**
    - **URL:** /train/add-train/
    - **Method:** POST
    - **Headers:** Authorization: Bearer ```<access_token>```
    - **Request Body:**
      ```json
      {
          "train_name": "Shatabdi Express",
          "source": "Delhi",
          "destination": "Mumbai",
          "train_capacity": 10
      }
      ```
    - **Response:**
        ```json
        {
            "message": "Train added successfully"
        }
        ```
4. **Get Trains**
    - **URL:** /train/get-trains/
    - **Method:** GET
    - **Request Body:**
      ```json
      {
          "source": "Jaipur",
          "destination": "Mumbai"
      }
      ```
    - **Response:**
        ```json
        [
            {
                "train_id": "10d37399-97f6-4ce3-ac2f-c8d879cc902d",
                "train_name": "Duranto Express",
                "train_capacity": 10,
                "remaining_capacity": 10,
                "is_full": false,
                "source": "Jaipur",
                "destination": "Mumbai",
                "seat_available": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10
                ]
            },
            {
                "train_id": "95198504-1e9a-4c41-b199-783d37169334",
                "train_name": "Bandra Terminus SF",
                "train_capacity": 10,
                "remaining_capacity": 10,
                "is_full": false,
                "source": "Jaipur",
                "destination": "Mumbai",
                "seat_available": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10
                ]
            }
        ]
        ```
5. **Book Ticket**
    - **URL:** /train/book-ticket/
    - **Method:** POST
    - **Headers:** Authorization: Bearer ```<access_token>```
    - **Request Body:**
      ```json
      {
          "train_id": "10d37399-97f6-4ce3-ac2f-c8d879cc902d",
          "seat_number": 5
      }
      ```
    - **Response:**
        ```json
        
        {
            "seat_id": "f03d877c-d915-4626-9744-c6dcfdb3c773",
            "message": "Seat locked successfully. Confirm booking to book the seat"
        }
        ```
    - If the seat is already locked by another user
        ```json
        {
            "error": "Seat is already locked"
        }
        ```
        This will seat will remain locked for 3 minutes until the booking is confirmed by hitting the ```confirm-booking``` API else the seat will be unlocked after 3 minutes.
        When the seat is locked by the user the seat_id is stored in the Redis cache and that seat number won't be displayed in the seat_available list of the train when ```get-train``` api is called until the booking is confirmed or that key is expired in the Redis cache.
6. **Confirm Booking**
    - **URL:** /train/confirm-booking/
    - **Method:** POST
    - **Headers:** Authorization: Bearer ```<access_token>```
    - **Request Body:**
      ```json
      {
          "seat_id": "f03d877c-d915-4626-9744-c6dcfdb3c773"
      }
      ```
    - **Response:**
        ```json
        {
            "message": "Seat booked successfully"
        }
        ```
7. **Get Booking History**
    - **URL:** /train/view-bookings/
    - **Method:** GET
    - **Headers:** Authorization Bearer ```<access_token>```
    - **Response:**
        ```json
        [
            {
                "train_id": "10d37399-97f6-4ce3-ac2f-c8d879cc902d",
                "train_name": "Duranto Express",
                "seat_number": 2,
                "source": "Jaipur",
                "destination": "Mumbai"
            },
            {
                "train_id": "10d37399-97f6-4ce3-ac2f-c8d879cc902d",
                "train_name": "Duranto Express",
                "seat_number": 5,
                "source": "Jaipur",
                "destination": "Mumbai"
            }
        ]
        ```

## Assumptions 
- The user can book only one seat at a time.

## SQLite Database Schema
- **User**
    - id
    - username
    - email
    - password
    - is_admin
- **Train**
    - id
    - train_name
    - source
    - destination
    - train_capacity
- **Seat**
    - id
    - train_id (Foreign Key to Train)
    - seat_number
    - is_booked
    - user (Foreign Key to User)

You can find the database schema in the ```models.py``` file in the ```train``` app and in the ```models.py``` file in the ```user``` app.

You can also use the Django Shell to interact with the database. Run the following command to open the Django shell
```bash
python manage.py shell
```
And then use the following queries to interact with the database
```python
from train.models import Train
from user.models import User
from train.models import Seat

# To get all the trains
trains = Train.objects.all()

# To get all the users
users = User.objects.all()

# To get all the seats
seats = Seat.objects.all()
```




    
