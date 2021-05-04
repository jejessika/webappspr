def baseline_poly_manual(data_x, svg_y):
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.ndimage import interpolation

    plt.plot(data_x, svg_y)
    plt.title('Pilih 10 titik untuk generate baseline', color = 'red', fontsize = 16)
    plt.xlabel('Time', fontsize=10)
    plt.ylabel('R.U', fontsize=10)
    point = plt.ginput(10, show_clicks=True, mouse_add=1, mouse_pop=3)
    plt.close(1)
    dt = np.dtype('float,float')
    arr = np.array(point, dtype=dt)
    x = arr['f0']
    y = arr['f1']

    # Importing Linear Regression
    from sklearn.linear_model import LinearRegression
    # importing libraries for polynomial transform
    from sklearn.preprocessing import PolynomialFeatures
    # for creating pipeline
    from sklearn.pipeline import Pipeline

    # creating pipeline and fitting it on data
    Input = [('polynomial', PolynomialFeatures(degree=4)), ('modal', LinearRegression())]
    pipe = Pipeline(Input)
    pipe.fit(x.reshape(-1, 1), y.reshape(-1, 1))

    poly_pred = pipe.predict(data_x.reshape(-1, 1))
    # sorting predicted values with respect to predictor
    sorted_zip = sorted(zip(data_x, poly_pred))
    x_poly, poly_pred = zip(*sorted_zip)

    x_poly = np.asarray(x_poly, dtype=int)
    poly_pred = np.asarray(poly_pred, dtype=float)
    poly_pred = poly_pred[:, 0]

    plt.plot(data_x, svg_y)
    plt.plot(data_x, poly_pred, color='orange', label='Hasil Prediksi Baseline')
    plt.xlabel('Time', fontsize=10)
    plt.ylabel('R.U', fontsize=10)
    plt.legend()
    plt.pause(3)
    plt.close()

    return poly_pred