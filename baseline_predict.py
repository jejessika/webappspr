def baseline_prediction(data_x, svg_y, result_y):
    import numpy as np
    from scipy.ndimage import interpolation
    import matplotlib.pyplot as plt

    y = np.copy(svg_y)
    x = np.copy(data_x)

    p = 0
    element_del = []
    while p < (len(result_y) - 1):
        temp = np.arange(result_y[p] - 20, result_y[p + 1] + 20)
        element_del = np.append(element_del, temp)
        p += 2
    x = np.delete(x, element_del)
    y = np.delete(y, element_del)


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
    # reshape multi dimensional array to 1D array
    poly_pred = np.reshape(poly_pred, (np.product(poly_pred.shape),))

    plt.plot(data_x, svg_y)
    plt.plot(data_x, poly_pred, color='orange',label='Hasil Prediksi Baseline')
    plt.scatter(x, y, s=1, color="red")
    plt.xlabel('Time', fontsize=10)
    plt.ylabel('R.U', fontsize=10)
    plt.legend()
    plt.pause(3)
    plt.close()
    return poly_pred
