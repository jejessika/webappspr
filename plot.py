def plt_grafik(data_x, svg_y, lokasi_sample, base_y):
    import matplotlib.pyplot as plt
    # plot
    plt.plot(data_x, svg_y)
    plt.plot(data_x, base_y, color='orange',label='Hasil Prediksi Baseline')
    plt.axvspan(0, data_x[-1], facecolor='blue', alpha=1000)
    # plot Warna Pembeda Antar Respon
    for p in range(0,len(lokasi_sample)):
        temp = []
        temp = lokasi_sample[p].split(";",2)
        plt.axvspan(float(temp[0]), float(temp[1]), facecolor='red', alpha=1000)
    plt.legend()
    plt.show()