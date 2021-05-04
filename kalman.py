from filterpy.kalman import KalmanFilter
import numpy as np

#====================================================

#-- Kalman Filter --

f = KalmanFilter (dim_x=2, dim_z=1)
f.x = np.array([[2289.],    # position
                [0.]])   # velocity
f.F = np.array([[1.,1.],
                [0.,1.]])

f.H = np.array([[1.,0.]])
p = 100.
f.P = np.array([[p,0.],
                [0.,p]])
f.R = 5
from filterpy.common import Q_discrete_white_noise
f.Q = Q_discrete_white_noise(dim=2, dt=0.1, var=0.13)

#===================================================

q = [] #variabel update

for z in range(0, 1413):
    f.predict()
    f.update(data)
    t = f.x[0]
    q.append(t)