import numpy as np
import pandas as pd

#check units
#check rk4 function - calculate by hand
#if by hand matches output, then find alternative function

# Define constants
g = 9.81  # Gravity (m/s^2)
rho = 1.225  # Air density at sea level (kg/m^3) #ideal gas law??? = pressure/(gas constant * air temperature)
Cd = 0.5  # Drag coefficient (adjust based on flap position)
A_base = 0.785 # 0.01  # Base cross-sectional area (m^2)
A_flaps = 0.00  # Additional area when flaps are fully deployed (m^2)
m = 17.24  # Mass of the rocket (kg)
dt = 0.1  # Time step (s)
gas_constant = 8.314 #j/(mol*K)
molar_mass = .029 #kg/mol

# Define drag force function
def drag(v, flap_position, pressure, air_temp):
    A = A_base + (flap_position / 100) * A_flaps  # Adjust area based on flap position
    rho = (pressure * molar_mass) / (gas_constant * (float(air_temp) + 273.15)) #celcius to kelvin
    #rho = (pressure * molar_mass) / (gas_constant * ( ( (float(air_temp) - 32) * (5/9) ) + 273.15 )) #farenheit to kelvin 
    return 0.5 * rho * v * v * Cd * A

# RK4 function for post-burnout
def rk4_step(t, h, v, flap_position, pressure, air_temp):
    def f(t, h, v):
        F_drag = drag(v, flap_position, pressure, air_temp)
        F_gravity = m * g
        dv_dt = -(F_drag + F_gravity) / m
        dh_dt = v
        return np.array([dh_dt, dv_dt])

    k1 = f(t, h, v)
    k2 = f(t + dt / 2, h + (k1[0] * dt )/ 2, v + k1[1] * dt / 2)
    k3 = f(t + dt / 2, h + (k2[0] * dt) / 2, v + k2[1] * dt / 2)
    k4 = f(t + dt, h + k3[0] * dt, v + k3[1] * dt)

    # Update altitude and velocity using RK4 formula
    h_next = h + (dt / 6) * (k1[0] + (2 * k2[0]) + (2 * k3[0]) + k4[0])
    v_next = v + (dt / 6) * (k1[1] + (2 * k2[1]) + (2 * k3[1]) + k4[1])

    return h_next, v_next

def get_sensor_data():
    #Replace with your path to the csv file
    path_to_data = r'C:\Users\samjo\OneDrive\Desktop\clubs\soar\airbrakes\test\dataset.csv'
    #path_to_data = r'C:\Programming\Git\Python\SOAR\University_of_South_Florida (2) (1).csv'
    sensorData = pd.read_csv(path_to_data)
    return sensorData[['Time', 'Altitude', 'Pressure', 'Velocity', 'Temperature']]

sensorData = get_sensor_data()

flap_position = 0  # Start with flaps retracted
#Looping from index of end of burnout to index of apogee in data set
index = 96
while index <= 377:
    t = sensorData.iloc[index,0]
    h = sensorData.iloc[index, 1]
    press = sensorData.iloc[index, 2]
    v = sensorData.iloc[index, 3]
    temp = sensorData.iloc[index, 4]

    # Run the RK4 loop for prediction
    while v > 0:  # While the rocket is ascending
        #hPa * 100 = Pascals
        h, v = rk4_step(t, h, v, flap_position, (press*100), temp)
        t += dt

    print(f"Time: {t:.3f}   Alt: {h:.5f}    Vel: {v:.3f}  Index: {index}\n")
    index += 1
#Real apogee from data set
print(f'Real Apogee: 4877.627')

# At the end of loop, h should be close to predicted apogee
