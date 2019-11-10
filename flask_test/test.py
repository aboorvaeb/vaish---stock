from flask import Flask, render_template, url_for, request, redirect

import monte_carlo as mc

app = Flask(__name__)


@app.route('/')
def index():
    value = 5	
    return render_template('index.html', x = value)

@app.route('/display',methods = ['POST','GET'])
def display():
    if request.method == "POST" :
            ticker1 = request.form['ticker']
            sim_days1 = request.form['sim_days']
            sim_num1 = request.form['sim_num']

            sim = mc.monte_carlo(ticker1)
            sim.plot_historical_data()
            a1,b1 = sim.brownian_motion(int(sim_days1,10),int(sim_num1,10))



            return render_template('display.html', a=a1,b=b1)
            #return ticker
    else :
    	return 'lol'

if __name__ == "__main__":
    app.run(debug=True)