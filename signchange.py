import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from despike1 import despike
from ma import ma
from scipy.signal import savgol_filter



data = pd.read_excel(r'C:\Users\kaprodi\Desktop\websignal-master-Signal\Signal\pbs+.xlsx')
data_numpy = data.to_numpy().transpose()
data_y = data_numpy[1]
data_x = data_numpy[0]

dspk_y = despike(data_y,50)

# moving average filter
ma_y = ma(dspk_y,9)

# savitzky-golay filter
svg_y = savgol_filter(ma_y, window_length=41, polyorder=1,deriv=0)

grad_y = np.gradient(svg_y)
asign = np.sign(grad_y)
signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)


signchange_coor = [0]
for i in range(0,len(signchange)):
    if signchange[i] == 1 :
        temp = i
        signchange_coor.append(temp)

plt.plot(data_x,svg_y)

for i in range(1,len(signchange_coor)):
    if i%2 == 0 :
        t_in = data_x[signchange_coor[i-1]]
        t_out = data_x[signchange_coor[i]]
        plt.axvspan(t_in, t_out, facecolor='red', alpha=1000) 
    else:
        t_in = data_x[signchange_coor[i-1]]
        t_out = data_x[signchange_coor[i]]
        plt.axvspan(t_in, t_out, facecolor='blue', alpha=1000) 
plt.show()
        