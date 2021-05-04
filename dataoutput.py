# Fungsi untuk memasukkan array yang berisi data hasil algoritma ke dalam dataframe
# Fungsi mengembalikan dataframe

def output(data_x, svg_y, lokasi_sample, jenis, konsentrasi):
    import pandas as pd
    
    d = dict( A = data_x, B = svg_y, C = lokasi_sample, D = jenis, E = konsentrasi)
    dataset = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in d.items()]))

    return dataset