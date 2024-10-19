import datetime
import queue

class Passenger:
    def __init__(self, name, email, phone_number):
        self.name = name
        self.email = email
        self.phone_number = phone_number

class Seat:
    def __init__(self, seat_number, is_booked=False):
        self.seat_number = seat_number
        self.is_booked = is_booked
.
class Node:
    def __init__(self, seat):
        self.seat = seat
        self.left = None
        self.right = None

class Flight:
    def __init__(self, flight_number, departure, arrival, departure_time, arrival_time, total_seats):
        self.flight_number = flight_number
        self.departure = departure
        self.arrival = arrival
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.total_seats = total_seats
        self.seat_map = self.initialize_seat_map(total_seats)
        self.passengers = {}  # Hash table for passenger information
        self.waitlist = queue.Queue()  # Queue for waitlist management
        self.bookings = 0  # Number of bookings

    def initialize_seat_map(self, total_seats):
        seat_map = Node(Seat("1A"))
        current = seat_map
        for i in range(2, total_seats + 1):
            new_seat = Node(Seat(f"{i}A"))
            current.right = new_seat
            current = new_seat
        return seat_map

    def assign_seat(self, passenger):
        current = self.seat_map
        while current:
            if not current.seat.is_booked:
                current.seat.is_booked = True
                self.passengers[passenger.email] = current.seat.seat_number  # Map email to seat number
                self.bookings += 1
                print(f"Seat assigned to {passenger.name} with email {passenger.email}. Seat Number: {current.seat.seat_number}")
                return True
            current = current.right # Move to the next seat
        print("No seats available. Adding to waitlist.")
        self.waitlist.put(passenger)
        return False

    def manage_waitlist(self):
        if not self.waitlist.empty():
            passenger = self.waitlist.get()
            current = self.seat_map
            while current:
                if not current.seat.is_booked:
                    current.seat.is_booked = True
                    self.passengers[passenger.email] = current.seat.seat_number
                    self.bookings += 1
                    print(f"Seat assigned to {passenger.name} with email {passenger.email} from waitlist. Seat Number: {current.seat.seat_number}")
                    return
                current = current.right
            print("No seats available. Passenger remains on the waitlist.")

    def optimize_flight_schedule(self):
        # This is a simple example of optimizing flight schedules by sorting flights based on departure time
        flights = [self]
        flights.sort(key=lambda x: x.departure_time)
        for flight in flights:
            print(f"Flight Number: {flight.flight_number}, Departure Time: {flight.departure_time}")

    def cancel_booking(self, email):
        if email in self.passengers:
            seat_number = self.passengers[email]
            current = self.seat_map
            while current:
                if current.seat.seat_number == seat_number:
                    current.seat.is_booked = False
                    del self.passengers[email]
                    self.bookings -= 1
                    print(f"Booking cancelled for {email}. Seat Number: {seat_number}")
                    self.manage_waitlist()
                    return
                current = current.right
            print("Booking not found.")
        else:
            print("Booking not found.")

    def display_flight_details(self):
        if self.bookings > 0:
            print(f"Flight Number: {self.flight_number}")
            print(f"Departure: {self.departure}")
            print(f"Arrival: {self.arrival}")
            print(f"Departure Time: {self.departure_time}")
            print(f"Arrival Time: {self.arrival_time}")
            print(f"Total Seats: {self.total_seats}")
            print(f"Bookings: {self.bookings}")
            print("Passengers:")
            for email, seat_number in self.passengers.items():
                print(f"{email} - {seat_number}")
        else:
            print("No bookings available.")

def main():
    print("Available flights:")
    print("1. New York to Los Angeles")
    print("2. Los Angeles to New York")
    print("3. Chicago to Miami")
    print("4. Miami to Chicago")

    choice = input("Enter the number of your preferred flight: ")

    if choice == "1":
        flight = Flight("AA101", "New York", "Los Angeles", datetime.time(10, 0), datetime.time(13, 0), 10)
    elif choice == "2":
        flight = Flight("AA102", "Los Angeles", "New York", datetime.time(14, 0), datetime.time(17, 0), 10)
    elif choice == "3":
        flight = Flight("AA103", "Chicago", "Miami", datetime.time(12, 0), datetime.time(15, 0), 10)
    elif choice == "4":
        flight = Flight("AA104", "Miami", "Chicago", datetime.time(16, 0), datetime.time(19, 0), 10)
    else:
        print("Invalid choice. Exiting program.")
        return
    while True:
        print("\n1. Book a seat")
        print("2. Cancel a booking")
        print("3. Display flight details")
        print("4. Optimize flight schedule")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            phone_number = input("Enter your phone number: ")
            passenger = Passenger(name, email, phone_number)
            flight.assign_seat(passenger)
        elif choice == "2":
            email = input("Enter your email: ")
            flight.cancel_booking(email)
        elif choice == "3":
            flight.display_flight_details()
        elif choice == "4":
            flight.optimize_flight_schedule()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
