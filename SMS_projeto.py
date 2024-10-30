import random
import math
import time

# Function to generate numbers using the linear congruential generator
def generate_linear_congruential_numbers(a, c, m, seed, size):
    x = seed
    numbers = []
    for _ in range(size):
        x = (a * x + c) % m
        numbers.append(x / m)
    return numbers

# Function to calculate the average of a list
def calculate_average(lst):
    return sum(lst) / len(lst) if lst else 0

# Function to simulate customer arrivals
def simulate_customer_arrivals(average_customers):
    return average_customers

# Main simulation function
def simulate_day(simulation_time, average_service_time, average_customers, a, c, m, seed, simulation_mode):
    if average_customers <= 0:
        print("Error: Average number of customers must be greater than zero.")
        return

    arrival_rate = 1 / average_customers
    number_of_events = int(average_customers)
    random_numbers = generate_linear_congruential_numbers(a, c, m, seed, number_of_events)
    arrival_times = [-math.log(1.0 - rn) / arrival_rate for rn in random_numbers]

    total_arrivals = 0
    total_departures = 0
    current_time = 0
    queue = []
    counter_occupied = False
    next_departure_time = 0
    wait_times = []

    for arrival_time in arrival_times:
        total_arrivals += 1
        current_time += arrival_time

        if simulation_mode == 'real time':
            print(f"\nCustomer {total_arrivals} arrived")
            time.sleep(random.uniform(0.5, 2.0))  # Random pause

        if not counter_occupied:
            counter_occupied = True
            service_time = -math.log(1.0 - random.random()) * average_service_time
            next_departure_time = current_time + service_time

            if simulation_mode == 'real time':
                print(f"Counter: Occupied, serving Customer {total_arrivals} in {service_time:.2f} minutes")
                time.sleep(service_time)  # Simulate service time
            total_departures += 1
        else:
            queue.append(current_time)  # Customer entered the queue
            if simulation_mode == 'real time':
                print(f"Customer {total_arrivals} approached the counter, but it is occupied.")

        # Serve customers in the queue
        if counter_occupied and current_time >= next_departure_time:
            counter_occupied = False
            if queue:  # If there are customers in the queue
                next_customer = queue.pop(0)
                service_time = -math.log(1.0 - random.random()) * average_service_time
                next_departure_time = current_time + service_time

                if simulation_mode == 'real time':
                    print(f"Counter: Occupied, serving the next customer in {service_time:.2f} minutes")
                    time.sleep(service_time)  # Simulate service time
                total_departures += 1

    # Calculate statistics
    average_wait_time = calculate_average(wait_times)
    average_queue_length = len(queue) / total_arrivals if total_arrivals > 0 else 0
    server_occupancy = total_departures / simulation_time

    return {
        'total_arrivals': total_arrivals,
        'total_departures': total_departures,
        'average_wait_time': average_wait_time,
        'average_queue_length': average_queue_length,
        'server_occupancy': server_occupancy
    }

def main():
    print("Single Server Queue Simulation")
    simulation_time = float(input("Enter the simulation time (in minutes): "))
    average_service_time = float(input("Enter the average service time (in minutes): "))
    
    a = int(input("Enter the value of 'a' (multiplier): "))
    c = int(input("Enter the value of 'c' (increment): "))
    m = int(input("Enter the value of 'm' (modulus): "))
    seed = int(input("Enter the initial seed value (x0): "))
    
    average_customers = float(input("Enter the average number of customers per day: "))
    simulation_mode = input("Would you like to run the simulation in 'Real time' or 'Fast'? (real time/fast): ").strip().lower()

    result = simulate_day(simulation_time, average_service_time, average_customers, a, c, m, seed, simulation_mode)

    print("\nSimulation Statistics:")
    print(f'Total arrivals: {result["total_arrivals"]}')
    print(f'Total departures: {result["total_departures"]}')
    print(f'Average wait time: {result["average_wait_time"]:.2f} minutes')
    print(f'Average queue length: {result["average_queue_length"]:.2f}')
    print(f'Server occupancy: {result["server_occupancy"]:.2f}')

if __name__ == "__main__":
    main()
