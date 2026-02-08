import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Cod special pentru a găsi baza de date pe server
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'matequiz_2026.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ... restul modelelor tale (Rezultat) rămân la fel ...

class Rezultat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(100))
    email = db.Column(db.String(100))
    foto = db.Column(db.String(255))
    rol = db.Column(db.String(20))
    nota = db.Column(db.Float)
    materie = db.Column(db.String(50))
    data = db.Column(db.DateTime, default=datetime.now)

@app.route('/')
def home(): return render_template('index.html')

@app.route('/admin_panel')
def admin(): return render_template('admin.html')

@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.json
    nou = Rezultat(
        nume=data['nume'], email=data['email'], foto=data['foto'],
        rol=data['rol'], nota=float(data['nota']), materie=data['materie']
    )
    db.session.add(nou)
    db.session.commit()
    return jsonify({"status": "succes"})

@app.route('/get_all_data')
def get_all_data():
    res = Rezultat.query.order_by(Rezultat.data.desc()).all()
    return jsonify([{
        "nume": r.nume, "email": r.email, "foto": r.foto,
        "nota": r.nota, "materie": r.materie, "data": r.data.strftime("%d/%m %H:%M")
    } for r in res])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)