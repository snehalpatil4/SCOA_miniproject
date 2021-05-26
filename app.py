from flask import Flask,render_template,request
import URLFeatureExtraction
import pickle
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/getURL',methods=['GET','POST'])
def getURL():
    if request.method == 'POST':
        url = request.form['url']
        print(url)
        data = URLFeatureExtraction.featureExtraction(url)
        print(data)
        # data.pop('path')
        # data.pop('host')
        # data.pop('ASNno')
        # data.pop('safebrowsing')
        data_list = np.array(data).reshape(1, -1)
        print(data_list)
        RFmodel = pickle.load(open('MLP_model_.pkl', 'rb'))
        predicted_value = RFmodel.predict(data_list)
        print(predicted_value)
        if predicted_value == 0:    
            value = "Legitimate"
            return render_template("home.html",error=value)
        else:
            value = "Phishing"
            return render_template("home.html",error=value)


if __name__ == "__main__":
    app.run(debug=True)
