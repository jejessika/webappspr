from pyrebase import pyrebase
import collections
import firebase_admin
from firebase_admin import credentials

config = {
    "apiKey": "AIzaSyCL8AqkgupmScHROiU8E0cta9YYigdGTaY",
    "authDomain": "test1-a06b1.firebaseapp.com",
    "databaseURL": "https://test1-a06b1.firebaseio.com",
    "projectId": "test1-a06b1",
    "storageBucket": "test1-a06b1.appspot.com",
    "messagingSenderId": "383571108013",
    "appId": "1:383571108013:web:ef563e8adb802358db2624",
    "measurementId": "G-M38DQ6VRM7",
    "serviceAccount": "key.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()

from flask import *
from flask_admin import *

''' Dynamic Plot '''
import pandas as pd
import numpy as np
import urllib.request
from bokeh.plotting import figure
from flask import Flask, render_template, request
from bokeh.embed import components
from bokeh.models import BoxAnnotation, Legend, Label
from despike1 import despike
from ma import ma
import ruptures as rpt
from scipy.signal import savgol_filter
from datainput import input_sample
from dataoutput import output
from baseline_predict import baseline_prediction
from baseline_manual import baseline_poly_manual
import copy

app = Flask(__name__)
app.secret_key = "EB2017"

@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        ufile = request.files['ufile'] #Menyimpan file ke variabel
        fname = ufile.filename
        ftype = fname.split('.')[1] #Mengidentifikasi tipe file
        storage.child(ftype+'/'+fname).put(ufile) #Memasukkan file ke storage
        flink = storage.child(ftype+'/'+fname).get_url(None) #Mendapatkan URL dari file
        # Session untuk passing data dari halaman satu ke halaman lain
        session['flink'] = flink 
        session['ftype'] = ftype
        newdata = {"Pengujian": "18", "Pasien": "patientId18", "Tanggal": "23/07/20", "Hasil": "Negatif", "DataCSV": flink, "Type": ftype}
        session['data'] = newdata
        db.child("Tests").push(newdata)
        if (ftype == 'sp2') or (ftype == 'sp28'):
            return redirect(url_for('input_user'))
        else:
            return redirect(url_for('input_user2'))
    return render_template('index.html')

@app.route('/user', methods=['GET', 'POST'])
def input_user():
    if request.method == 'POST':
        # Menyimpan masukan dari pengguna ke dalam variabel
        baseline = request.values['baseline']
        sampel1 = request.values['sampel1']
        konsen1 = request.values['konsen1']
        sampel2 = request.values['sampel2']
        konsen2 = request.values['konsen2']
        sampel3 = request.values['sampel3']
        konsen3 = request.values['konsen3']
        sampel4 = request.values['sampel4']
        konsen4 = request.values['konsen4']

        session['baseline'] = baseline
        session['sampel1'] = sampel1
        session['konsen1'] = konsen1
        session['sampel2'] = sampel2
        session['konsen2'] = konsen2
        session['sampel3'] = sampel3
        session['konsen3'] = konsen3
        session['sampel4'] = sampel4
        session['konsen4'] = konsen4
        return redirect(url_for('grafik_baseline'))
    return render_template('input_user.html')

@app.route('/user2', methods=['GET', 'POST'])
def input_user2():
    if request.method == 'POST':
        baseline = request.values['baseline']
        session['baseline'] = baseline
        return redirect(url_for('grafik_baseline'))
    return render_template('input_user2.html')


@app.route('/recent_tests', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        keyId = request.form.get('keyId')
        session['keyId'] = keyId

        return redirect(url_for('testpage', keyId=keyId))
    dbase = db.child("Tests").get()
    return render_template('viewer.html', dbase = dbase)

@app.route('/grafik_baseline', methods = ['GET','POST'])
def grafik_baseline():
    if request.method == 'POST':
        if 'flink' in session:
            flink = session['flink']
            ftype = session['ftype']

            # baseline
            baseline = session['baseline']
            pilih_baseline = int(baseline)

            if (ftype == 'sp2') or (ftype == 'sp28'):
                a_file = urllib.request.urlopen(flink) #Read raw file
                list_of_lists = []
                # Konversi file raw menjadi list of lists
                for line in a_file:
                    stripped_line = line.strip()
                    line_list = stripped_line.split()
                    list_of_lists.append(line_list)

                a_file.close()

                # Mengubah list of lists menjadi suatu dataframe
                data = pd.DataFrame(list_of_lists)
                data.columns = ["time", "ch1", "ch2", "subsidiary", "difference"]
                # Konversi dari dataframe ke array
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

                if pilih_baseline == 1:
                    base_y = baseline_poly_manual(data_x, svg_y)
                    #return render_template('grafik_baseline.html', **baseline_poly_manual.kwargs)
                elif pilih_baseline == 2:
                    base_y = baseline_prediction(data_x, svg_y, result_y)
                    #return render_template('grafik_baseline.html', **baseline_prediction.kwargs)
            elif (ftype == 'csv') or (ftype == 'xls') or (ftype == 'xlsx'):
                if pilih_baseline == 1:
                    base_y = baseline_poly_manual(data_x, svg_y)
                elif pilih_baseline == 2:
                    base_y = baseline_prediction(data_x, svg_y, result_y)

    return redirect(url_for('content'))

@app.route('/result', methods = ['GET','POST'])
def content():
    if 'flink' in session:
        flink = session['flink']
        ftype = session['ftype']

        # baseline
        baseline = session['baseline']
        pilih_baseline = int(baseline)

        if (ftype == 'sp2') or (ftype == 'sp28'):
            sampel1 = session['sampel1']
            konsen1 = session['konsen1']
            sampel2 = session['sampel2']
            konsen2 = session['konsen2']
            sampel3 = session['sampel3']
            konsen3 = session['konsen3']
            sampel4 = session['sampel4']
            konsen4 = session['konsen4']

            a_file = urllib.request.urlopen(flink)

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
            a = 1
            lokasi_sample = []
            for p in range(1,len(mean_sampel)):
                if mean_sampel[p-1]<mean_sampel[p] :
                    t_in = data_x[result_y[p-1]]
                    t_out = data_x[result_y[p]]
                    lokasi_sample.append(str(t_in) + ";" + str(t_out))
                    a += 1

            #Input Jenis Pengujian dan Konsentrasi Analit
            jenis, konsentrasi = input_sample(sampel1,konsen1,sampel2,konsen2,sampel3,konsen3,sampel4,konsen4)
            
            df = output(data_x, svg_y, lokasi_sample, jenis, konsentrasi)
            x = df['A']
            y = df['B']

        elif ftype == 'csv':
            df = pd.read_csv(flink, usecols = [0,1,2,3,4], names = ['A','B','C','D','E'])
            x = df['A']
            y = df['B']
            data_numpy = df.to_numpy().transpose()
            data_y = data_numpy[1][0:len(data_numpy[1])]
            data_y = np.asfarray(data_y,float)
            data_x = data_numpy[0][0:len(data_numpy[0])]
            data_x = np.asfarray(data_x,float)
            # change points detection 
            chgpts_y = rpt.Pelt(model='l2').fit(data_y)
            result_y = chgpts_y.predict(pen=5000)
            if pilih_baseline == 1:
                base_y = baseline_poly_manual(data_x, data_y)
            elif pilih_baseline == 2:
                base_y = baseline_prediction(data_x, data_y, result_y)

        elif (ftype == 'xlsx') or (ftype == 'xls'):
            df = pd.read_excel(flink, usecols = [0,1,2,3,4], names = ['A','B','C','D','E'])
            x = df['A']
            y = df['B']
            data_numpy = df.to_numpy().transpose()
            data_y = data_numpy[1][0:len(data_numpy[1])]
            data_y = np.asfarray(data_y,float)
            data_x = data_numpy[0][0:len(data_numpy[0])]
            data_x = np.asfarray(data_x,float)
            # change points detection 
            chgpts_y = rpt.Pelt(model='l2').fit(data_y)
            result_y = chgpts_y.predict(pen=5000)
            if pilih_baseline == 1:
                base_y = baseline_poly_manual(data_x, data_y)
            elif pilih_baseline == 2:
                base_y = baseline_prediction(data_x, data_y, result_y)


        # Get sample concentration by splitting the 'konsentrasi' column
        def concentration_label(konsen,i):
            for column in df[[konsen]]:
                columnSeriesObj = df[column]
                temp = columnSeriesObj.values[i].split(";",2)
                return temp[0]

        #Add Tooltips:
        TOOLTIPS = [
            ("Index", "$index"),
            ("Time (s)", "$x"),
            ("Refractive Unit (RU)", "$y"),
        ]

        #Add plot
        p= figure(title="Data SPR Hasil Algoritma [Normalized]", x_axis_label="Time (s)", y_axis_label="Refractive Unit (RU)", tooltips = TOOLTIPS, toolbar_location = "above", tools = "pan, hover, box_zoom, reset, wheel_zoom")
            
        #Render glyph
        #Put the legend outside of the plot
        legend = Legend(items=[
            ("Channel 1", [p.line(x,y, line_width=3, muted_alpha = 0.2)]),("Baseline", [p.line(x,base_y, line_width=2, muted_alpha = 0.2, color = 'red')])
        ], location="center")
        p.add_layout(legend, 'right')
        p.legend.click_policy="mute"

        # Customize the plot
        p.background_fill_color = "beige"
        p.toolbar.logo = None

        # Setting bands and labels to distinguish each response
        for column in df[['C']]:
            columnSeriesObj = df[column]
            for i in range(0,columnSeriesObj.count()):
                temp = []
                temp = str(columnSeriesObj.values[i]).split(";",2)

                # Add red band between t_in and t_out specified in csv file
                red_box = BoxAnnotation(left=float(temp[0]), right=float(temp[1]), fill_color='red', fill_alpha=0.2)
                p.add_layout(red_box)

                # Add label for each red band
                mark = Label(x=float(temp[0]), y=(df.loc[df.loc[df['A'] == float(temp[0])].index[0],"B"]),
                 text=df['D'].values[i]+ ' ' +concentration_label('E',i) + ' ng/mL', text_font_size = '8pt', render_mode='canvas', border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)
                p.add_layout(mark)

                #Reflectivity average between each response
                jumlah = 0
                count = 0
                for j in range(df.loc[df['A'] == float(temp[0])].index[0],1+(df.loc[df['A'] == float(temp[1])].index[0])):
                    jumlah += y.values[j]
                    count += 1
                avg = round(jumlah/count)

                #Find the maximum value of RU for each response
                ru_max = df.loc[(df.loc[df['A'] == float(temp[0])].index[0]):(1+(df.loc[df['A'] == float(temp[1])].index[0])), 'B'].max()

                avg_mark = Label(x=float(temp[0]),
                         y=ru_max,
                         text='RU avg = '+str(avg), text_font_size = '8pt',
                         render_mode='canvas', border_line_color='black', border_line_alpha=1.0,
                         background_fill_color='white', background_fill_alpha=1.0)
                p.add_layout(avg_mark)

        #Menyematkan grafik ke file HTML
        script, div = components(p)
        kwargs = {'script': script, 'div': div}
        kwargs['title'] = 'bokeh-with-flask'
        data = session['data']
        return render_template('content.html', **kwargs, data=data)
        
    else:
        return render_template('index.html')


''' Test '''
@app.route('/test=<keyId>')
def testpage(keyId):
    keyId = session['keyId']
    data = db.child("Tests").child(keyId).get().val()
    flink = db.child("Tests").child(keyId).child("DataCSV").get().val()
    ftype = db.child("Tests").child(keyId).child("Type").get().val()
    session['data'] = data
    session['flink'] = flink
    session['ftype'] = ftype
    if (ftype == 'sp2') or (ftype == 'sp28'):
        return render_template('input_user.html')
    else:
        return render_template('input_user2.html')



if __name__ == "__main__":
    app.run(debug=True)