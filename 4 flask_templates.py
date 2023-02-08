from flask import Flask, render_template

app = Flask(__name__)

@app.route("/inicio")
def inicio():
    return render_template('inicio.html',nombre='eduardo', edad = 35)

app.run(debug=True)