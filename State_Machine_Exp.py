import numpy as np
import csv

# Open the CSV file
with open('imu_data.csv', mode='r') as file:
    reader = csv.DictReader(file)  # Read CSV into a dictionary for easier column access
    acceleration = []

    # Extract columns
    for row in reader:
        acceleration.append(row[' accel_y'])
        
with open('University_of_South_Florida (2) (1).csv', mode='r') as file:
    reader = csv.DictReader(file)  # Read CSV into a dictionary for easier column access
    velocity = []
    altitude = []

    # Extract columns
    for row in reader:
        velocity.append(row['Velocity'])
        altitude.append(row['Altitude'])
        
def RunPID():
    x = np.random.rand()
    return x

# Initial parameters
for A in range(1000):
    while (0 < A < 1000):
        previousM1state = 1
        currentV = int(float(velocity[A]))  # initial upward velocity
        currentA = int(float(acceleration[A]))  # initial acceleration
        currentH = int(float(altitude[A]))   # starts from the ground
        h2 = 4000       # target height for transitioning to state 4
        statesM1 = np.array([1, 2, 2, 3, 3, 4, 4])

        # History to track state transitions
        history = []

        # Simulation loop
        for t in range(1):  # Adjust steps as needed
            # Set states and conditions without modification
            
            M1 = np.array([
                (previousM1state == 1) & (currentA >= 0) & (currentV > 0) & (currentH < h2), # Stage 1 to Stage 1
                (previousM1state == 1) & (currentA < 0) & (currentV > 0) & (currentH < h2), # Stage 1 to Stage 2
                (previousM1state == 2) & (currentA < 0) & (currentV > 0) & (currentH < h2), # Stage 2 to Stage 2
                (previousM1state != 2) & (currentV > 0) & (currentA < 0) & (currentH > h2), # Stage 2 to Stage 3
                (previousM1state != 3) & (-300 < currentV < 300 ) & (currentH > h2), # Stage 3 to Stage 3
                (previousM1state != 3) & (currentA < 0) & (currentV < 0) & (currentH <= h2), # Stage 3 to Stage 4
                (previousM1state != 4) & (currentA < 0) & (currentV < 0) & (currentH < h2) #Stage 4 to Stage Stage 4
            ])

            # Determine the current state based on conditions
            currentM1State = statesM1[np.argmax(M1)]
            previousM1state = currentM1State  # Update state 

            
            # PID section
            if currentM1State == 2:
                X = RunPID()
            elif currentM1State == 3:
                X = 1
            else:
                X = 0

            # Record the state for later analysis
            history.append((currentM1State, currentV, currentA, currentH, X))

            # Update velocity, height, and potentially stop if the ball has landed
            currentH += currentV 
            currentV += currentA
            
            if (t > 10) & (currentA > -10):
                currentA -= 1

            if (t > 0) & (currentH <= 0):  # Ball hits the ground
                currentH = 0
                currentV = 0
                currentA = 0
                break  # End simulation when the ball lands
            # Print simulation results
            for step, (statesM1, V, A, H, X) in enumerate(history):
                print(f"Step {step}: Rocket Stage={statesM1}, Velocity={V}, Acceleration={A}, Height={H}, PID State = {X}")
