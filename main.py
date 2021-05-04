import numpy as np
import pandas as pd
from despike1 import despike
from ma import ma
import ruptures as rpt
from scipy.signal import savgol_filter
from datainput import input_sample
from dataoutput import output
from plot import plt_grafik
from baseline_predict import baseline_prediction
from baseline_manual import baseline_linear_manual, baseline_poly_manual


# input data
a_file = open("190520.sp2", "r")

list_of_lists = []
for line in a_file:
  stripped_line = line.strip()
  line_list = stripped_line.split()
  list_of_lists.append(line_list)

a_file.close()

data = pd.DataFrame(list_of_lists)
data.columns = ["time", "ch1", "ch2", "subsidiary", "difference"]

data_numpy = data.to_numpy().transpose()
data_y = data_numpy[1][0:len(data_numpy[1])]
data_y = np.asfarray(data_y,float)
data_x = data_numpy[0][0:len(data_numpy[0])]
data_x = np.asfarray(data_x,float)

# menghilangkan outliers
dspk_y = despike(data_y,50)

# moving average filter
ma_y = ma(dspk_y,9)

# savitzky-golay filter
svg_y = savgol_filter(ma_y, window_length=41, polyorder=2)


# change points detection 
chgpts_y = rpt.Pelt(model='l2').fit(svg_y)
result_y = chgpts_y.predict(pen=5000)


# baseline
print("Baseline Manual/Otomatis?")
print('1. Baseline Manual','\n','2. Baseline Otomatis','\n')
pilih_baseline = int(input())
if pilih_baseline == 1:
    base_y = baseline_poly_manual(data_x, svg_y)
elif pilih_baseline == 2:
    base_y = baseline_prediction(data_x, svg_y, result_y)


#mean
mean_sampel = []
dx = 10
j = 0 + dx
for i in range(0,len(result_y)):
    temp = sum(svg_y[j:result_y[i]-dx])/len(svg_y[j:result_y[i]-dx])
    mean_sampel.append(temp)
    j = result_y[i] + dx

#mean sampel
sampel = []
for l in range(1,len(result_y)):
    if (mean_sampel[l-1] < mean_sampel[l]):
        temp = mean_sampel[l]
        sampel.append(temp)

#lokasi sample
print('')
print('Waktu Sampel')
a = 1
lokasi_sample = []
for p in range(1,len(mean_sampel)):
    if mean_sampel[p-1]<mean_sampel[p] :
        t_in = data_x[result_y[p-1]]
        t_out = data_x[result_y[p]]
        print('Sampel ',a,' | Mulai ',t_in,'s | Berhenti ',t_out,'s | Durasi ',t_out-t_in,'s')
        lokasi_sample.append(str(t_in) + ";" + str(t_out))
        a += 1

print(" ")

#Input Jenis Pengujian dan Konsentrasi Analit
jenis, konsentrasi = input_sample(len(sampel))

for m in range(0, len(sampel)):
    print('sampel ', m + 1, ' = ', sampel[m])

output(data_x, svg_y,lokasi_sample, jenis, konsentrasi)
plt_grafik(data_x, svg_y, lokasi_sample, base_y)
