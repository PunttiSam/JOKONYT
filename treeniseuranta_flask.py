
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

data_file = "treenidata.csv"

if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Päivämäärä", "Treenipäivä", "Liike", "Paino (kg)", "Toistot"])
    df.to_csv(data_file, index=False)

@app.route('/')
def index():
    df = pd.read_csv(data_file)
    return '''
    <html>
    <head><title>Treeniseuranta</title></head>
    <body>
        <h1>Treeniseuranta</h1>
        <form action="/add" method="post">
            <label>Treenipäivä:</label>
            <select name="treenipaiva">
                <option>Työntävät</option>
                <option>Vetävät</option>
                <option>Jalat</option>
                <option>Extra</option>
            </select>
            <br>
            <label>Liike:</label>
            <input type="text" name="liike">
            <br>
            <label>Paino (kg):</label>
            <input type="number" name="paino" step="0.5">
            <br>
            <label>Toistot:</label>
            <input type="number" name="toistot" min="1">
            <br>
            <input type="submit" value="Tallenna">
        </form>
        <h2>Tallennetut harjoitukset</h2>
        <table border="1">
            <tr><th>Päivämäärä</th><th>Treenipäivä</th><th>Liike</th><th>Paino (kg)</th><th>Toistot</th></tr>
            {}
        </table>
    </body>
    </html>
    '''.format(''.join([
        f"<tr><td>{r['Päivämäärä']}</td><td>{r['Treenipäivä']}</td><td>{r['Liike']}</td><td>{r['Paino (kg)']}</td><td>{r['Toistot']}</td></tr>"
        for _, r in df.iterrows()]))

@app.route('/add', methods=['POST'])
def add():
    treenipaiva = request.form["treenipaiva"]
    liike = request.form["liike"]
    paino = request.form["paino"]
    toistot = request.form["toistot"]

    df = pd.read_csv(data_file)
    df = df.append({"Päivämäärä": pd.Timestamp.now().strftime("%Y-%m-%d"),
                    "Treenipäivä": treenipaiva,
                    "Liike": liike,
                    "Paino (kg)": paino,
                    "Toistot": toistot}, ignore_index=True)
    df.to_csv(data_file, index=False)
    
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
