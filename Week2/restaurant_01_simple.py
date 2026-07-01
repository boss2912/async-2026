from time import sleep, ctime, time

#Greeting synchronous
def greet_diners(customer):
    print(f"{ctime()} -> Greeting for Customer {customer}...")
    sleep(1)  # Simulate a delay in greeting
    print(f"{ctime()} -> Greeting for Customer {customer} ...Done!")
    
def take_order(customer):
    print(f"{ctime()} -> Taking Order for Customer {customer}...")
    sleep(1)  # Simulate a delay in taking order
    print(f"{ctime()} -> Taking Order for Customer {customer} ...Done!")
    
def do_cooking(customer):
    print(f"{ctime()} -> Cooking for Customer {customer}...")
    sleep(1)  # Simulate a delay in cooking
    print(f"{ctime()} -> Cooking for Customer {customer} ...Done!")
    
def mini_bar(customer):
    print(f"{ctime()} -> Mini Bar for Customer {customer}...")
    sleep(1)  # Simulate a delay in preparing mini bar
    print(f"{ctime()} -> Mini Bar for Customer {customer} ...Done!")
    
if __name__ == "__main__":
    customers = ["A", "B", "C"]
    
    start_time = time()
    
    for customer in customers:
        greet_diners(customer)
        take_order(customer)
        do_cooking(customer)
        mini_bar(customer)
        
duration = time() - start_time
print(f"{ctime()} finished Cooking in {duration:.2f} seconds")  # Will be