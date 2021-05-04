def input_sample(s1,k1,s2,k2,s3,k3,s4,k4):
    jenis_sample = []
    konsentrasi = []
    '''
    jenis_sample.append(s1)
    konsentrasi.append(k1 + ";NaN")
    '''

    if s1 == '1':
        jenis_sample.append('RBD')
        konsentrasi.append(k1 + ";NaN")
    elif s1 == '2':
        jenis_sample.append('IBV')
        konsentrasi.append(k1 + ";NaN")
    elif s1 == '3':
        jenis_sample.append('Non-Spesifik')
        konsentrasi.append(k1 + ";NaN")
    elif s1 == '4':
        jenis_sample.append('Unknown')
        konsentrasi.append(k1 + ";NaN")

    if s2 == '1':
        jenis_sample.append('RBD')
        konsentrasi.append(k2 + ";NaN")
    elif s2 == '2':
        jenis_sample.append('IBV')
        konsentrasi.append(k2 + ";NaN")
    elif s2 == '3':
        jenis_sample.append('Non-Spesifik')
        konsentrasi.append(k2 + ";NaN")
    elif s2 == '4':
        jenis_sample.append('Unknown')
        konsentrasi.append(k2 + ";NaN")

    if s3 == '1':
        jenis_sample.append('RBD')
        konsentrasi.append(k3 + ";NaN")
    elif s3 == '2':
        jenis_sample.append('IBV')
        konsentrasi.append(k3 + ";NaN")
    elif s3 == '3':
        jenis_sample.append('Non-Spesifik')
        konsentrasi.append(k3 + ";NaN")
    elif s3 == '4':
        jenis_sample.append('Unknown')
        konsentrasi.append(k3 + ";NaN")

    if s4 == '1':
        jenis_sample.append('RBD')
        konsentrasi.append(k4 + ";NaN")
    elif s4 == '2':
        jenis_sample.append('IBV')
        konsentrasi.append(k4 + ";NaN")
    elif s4 == '3':
        jenis_sample.append('Non-Spesifik')
        konsentrasi.append(k4 + ";NaN")
    elif s4 == '4':
        jenis_sample.append('Unknown')
        konsentrasi.append(k4 + ";NaN")

    return jenis_sample, konsentrasi