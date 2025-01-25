from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
import os


app = Flask(__name__)
CORS(app, origins="http://localhost:5173")

# configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///propostas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Funcoes
# 1 Função para gerar PDF
def gerar_pdf_proposta(proposta):
    # criacao do objeto PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Cabeçalho
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Proposta", ln=True, align="C")
    pdf.ln(10)
    
    # detalhes da proposta
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=f"Cliente: {proposta.cliente}", ln=True)
    pdf.cell(200, 10, txt=f"Título: {proposta.titulo}", ln=True)
    pdf.cell(0, 10, txt=f"Descrição: {proposta.descricao}", ln=True)
    pdf.cell(0, 10, txt=f"Preço: R$ {proposta.preco:.2f}", ln=True)
    
    # Salvar PDF em um diretório
    if not os.path.exists("propostas_pdfs"):
        os.makedirs("propostas_pdfs")
    caminho_pdf = f"propostas_pdfs/proposta_{proposta.id}.pdf"
    pdf.output(caminho_pdf)
    
    return caminho_pdf
# Modelos
#3 Modelo de usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(100), nullable=False)
    
## Modelo de proposta
class Proposta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    cliente = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

# Rotas
## Rota inicial
@app.route('/')
def home():
    return "Bem vindo ao Gerador de Propostas!"


# rota para cadastro de usuário
@app.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    dados = request.json
    nome = dados.get('nome')
    email = dados.get('email')
    senha = generate_password_hash(dados.get('senha'))
    
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'erro': 'Email já cadastrado'}), 400
    
    novo_usuario = Usuario(nome=nome, email=email, senha=senha)
    db.session.add(novo_usuario)
    db.session.commit()
    
    return jsonify({"mensagem": "Usuário cadastrado com sucesso"})

# rota para login de usuário
@app.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    usuario = Usuario.query.filter_by(email=email).first()
    
    if not usuario or not check_password_hash(usuario.senha, senha):
        return jsonify({'erro': 'Email ou senha incorretos'}), 400
    
    return jsonify({"mensagem": "Login realizado com sucesso!"})

# TODO inserir para trazer o id do usuario de acordo com o usuário que estiver logado
# rota para criar uma proposta
@app.route('/proposta', methods=['POST'])
def criar_propostas():
    dados = request.json
    titulo = dados.get("titulo")
    descricao = dados.get('descricao')
    preco = dados.get('preco')
    cliente = dados.get('cliente')
    usuario_id = dados.get('usuario_id')

    nova_proposta = Proposta(
        titulo=titulo,
        descricao=descricao,
        preco=preco,
        cliente=cliente,
        usuario_id=usuario_id
    )
    db.session.add(nova_proposta)
    db.session.commit()
    
    return jsonify({"mensagem": "Proposta criada com sucesso!"})


# TODO Na rota para consultar a proposta alterar o id para o Nome do Usuário
# rota para listar as propostas de um usuário
@app.route('/propostas/<int:usuario_id>', methods=['GET'])
def listar_propostas(usuario_id):
    propostas = Proposta.query.filter_by(usuario_id=usuario_id).all()
    lista_propostas = [
        {
            "id": p.id,
            "titulo": p.titulo,
            "descricao": p.descricao,
            "preco": p.preco,
            "cliente": p.cliente
        } for p in propostas
    ]
    
    return jsonify(lista_propostas)

# rota para gerar PDF de uma proposta
@app.route('/proposta/pdf/<int:proposta_id>', methods=['GET'])
def baixar_pdf_proposta(proposta_id):
    proposta = Proposta.query.get(proposta_id)
    if not proposta:
        return jsonify({"erro": "Proposta não encontrada"}), 404
    
    caminho_pdf = gerar_pdf_proposta(proposta)
    
    return send_file(caminho_pdf, as_attachment=True)

# rota para deletar uma proposta
@app.route('/proposta/<int:proposta_id>', methods=['DELETE'])
def deletar_proposta(proposta_id):
    proposta = Proposta.query.get_or_404(proposta_id) # busca proposta ou retorna erro
    db.session.delete(proposta) # remove a proposta
    db.session.commit()

    return jsonify({'message':'Proposta deletada com sucesso!'})


# executando o app
if __name__ == "__main__":
    with app.app_context():
        db.create_all()     # cria as tabelas no banco de dados
    app.run(debug=True) 
    
