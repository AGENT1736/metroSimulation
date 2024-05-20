import simpy
import random

# Constants
TICKET_PRICE = 100
ITEMS = {
    1: 10,  # Item 1 costs 10
    2: 15,  # Item 2 costs 15
    3: 25,  # Item 3 costs 25
    4: 50,  # Item 4 costs 50
    5: 30   # Item 5 costs 30
}
TRAIN_INTERVALS = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
DESTINATIONS = [1, 2, 3, 4, 5]

def ticket_sales_service(env, customer):
    if not customer['ticket_purchased']:
        if customer['budget'] < TICKET_PRICE:
            print(f"Customer {customer['id']} at {env.now}: Insufficient funds for ticket!")
        else:
            customer['budget'] -= TICKET_PRICE
            customer['ticket_purchased'] = True
            print(f"Customer {customer['id']} at {env.now}: Ticket purchased. New budget = {customer['budget']}")
    yield env.timeout(1)

def cafeteria_service(env, customer, item):
    if item in ITEMS:
        if customer['budget'] >= ITEMS[item]:
            customer['budget'] -= ITEMS[item]
            print(f"Customer {customer['id']} at {env.now}: Purchased item {item} for {ITEMS[item]}. New budget = {customer['budget']}")
        else:
            print(f"Customer {customer['id']} at {env.now}: Insufficient funds for item {item}!")
    else:
        print(f"Customer {customer['id']} at {env.now}: Item {item} not found!")
    yield env.timeout(1)

def train_service(env, customer):
    random_schedule = random.choice(TRAIN_INTERVALS)
    print(f"Customer {customer['id']} at {env.now}: Train arrives in {random_schedule} minutes")
    yield env.timeout(random_schedule)
    print(f"Customer {customer['id']} at {env.now + random_schedule}: Customer {customer['id']} boards the train")

def directions(env, customer, num_questions, direction):
    for _ in range(num_questions):
        if direction == 1:
            print(f"Customer {customer['id']} at {env.now}: The ticket desk is at location 1")
        elif direction == 2:
            print(f"Customer {customer['id']} at {env.now}: The help desk is at location 2")
        elif direction == 3:
            print(f"Customer {customer['id']} at {env.now}: The restroom is at location 3")
        elif direction == 4:
            print(f"Customer {customer['id']} at {env.now}: The cafeteria is at location 4")
        elif direction == 5:
            print(f"Customer {customer['id']} at {env.now}: The trains are at location 5")
    yield env.timeout(1)

def customer_process(env, customer):
    yield env.process(ticket_sales_service(env, customer))
    if customer['ticket_purchased']:
        yield env.process(cafeteria_service(env, customer, random.choice(list(ITEMS.keys()))))
        yield env.process(directions(env, customer, random.randint(1, 3), random.choice(DESTINATIONS)))
        yield env.process(train_service(env, customer))

def setup(env, num_customers):
    for i in range(num_customers):
        customer = {
            'id': i,
            'budget': random.randint(50, 200),
            'ticket_purchased': False
        }
        env.process(customer_process(env, customer))
    yield env.timeout(0)

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, 5))

# Run the simulation for 3 hours (180 minutes)
env.run(until=180)
