from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3

                                                                                                                                       
app = Flask(__name__)    

@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #com

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogram():
    return render_template("histogram.html")
  
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return jsonify({'minutes': date_object.minute})

@app.route('/commits/')
def commits():
    # Récupère les 30 derniers commits du repo
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    response = requests.get(url)
    data = response.json()

    # Extraction des minutes de chaque commit
    minutes = []
    for commit in data:
        try:
            date_str = commit["commettre"]["auteur"]["date"]  # clé à respecter
            date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minutes.append(date_obj.minute)
        except KeyError:
            continue  # Ignore les commits mal formés

    # Compte des commits par minute
    counts = [minutes.count(i) for i in range(60)]

    # On envoie le tableau counts au template HTML
    return render_template("commits.html", counts=counts)


  
if __name__ == "__main__":
  app.run(debug=True)
