from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafearoma.db'
db = SQLAlchemy(app)


class CLIENTE(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True)
    cpf = db.Column(db.String(14), unique=True)
    endereco = db.Column(db.String(255))
    data_cadastro = db.Column(db.DateTime(), default=datetime.now)

# CRUD - READ (ler)
@app.route('/')
def index():
    clientes = CLIENTE.query.all()
    return render_template('index.html', clientes=clientes)

# CRUD - Create (criar)
@app.route('/create', methods=['POST'])
def create_cliente():

    nome = request.form['nome']
    telefone = request.form['telefone']
    email = request.form['email']
    cpf = request.form['cpf']
    endereco = request.form['endereco']

    novo_cliente = CLIENTE(nome=nome, telefone=telefone, email=email, cpf=cpf, endereco=endereco)

    db.session.add(novo_cliente)
    db.session.commit()

    return redirect('/')


# CRUD - Update (atualizar)
@app.route('/update/<int:id_cliente>', methods=['POST'])
def update_cliente(id_cliente):

    cliente = CLIENTE.query.get(id_cliente)

    if cliente:
        cliente.nome = request.form['nome']
        cliente.telefone = request.form['telefone']
        cliente.email = request.form['email']
        cliente.cpf = request.form['cpf']
        cliente.endereco = request.form['endereco']
        db.session.commit()

    return redirect('/')
    

# CRUD - Delete (apagar)
@app.route('/delete/<int:id_cliente>', methods=['POST'])
def delete_cliente(id_cliente):
    
    cliente = CLIENTE.query.get(id_cliente)

    if cliente:
        db.session.delete(cliente)
        db.session.commit()

        return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5153)