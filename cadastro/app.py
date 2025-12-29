from flask import Flask, request, jsonify, session
from flask_cors import CORS
import sqlite3
import hashlib
import secrets
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Chave secreta para sessões
CORS(app)  # Permite requisições do front-end

# Criar banco de dados e tabela de usuários
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            data_cadastro TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para criptografar senha
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Rota de cadastro
@app.route('/cadastro', methods=['POST'])
def cadastro():
    try:
        dados = request.get_json()
        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')
        
        # Validações básicas
        if not nome or not email or not senha:
            return jsonify({'sucesso': False, 'mensagem': 'Todos os campos são obrigatórios'}), 400
        
        if len(senha) < 6:
            return jsonify({'sucesso': False, 'mensagem': 'Senha deve ter no mínimo 6 caracteres'}), 400
        
        # Conectar ao banco
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Verificar se email já existe
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({'sucesso': False, 'mensagem': 'Email já cadastrado'}), 400
        
        # Inserir novo usuário
        senha_hash = hash_senha(senha)
        data_cadastro = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT INTO usuarios (nome, email, senha, data_cadastro)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, senha_hash, data_cadastro))
        
        conn.commit()
        conn.close()
        
        return jsonify({'sucesso': True, 'mensagem': 'Cadastro realizado com sucesso!'}), 201
        
    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': f'Erro no servidor: {str(e)}'}), 500

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    try:
        dados = request.get_json()
        email = dados.get('email')
        senha = dados.get('senha')
        
        if not email or not senha:
            return jsonify({'sucesso': False, 'mensagem': 'Email e senha são obrigatórios'}), 400
        
        # Conectar ao banco
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Buscar usuário
        senha_hash = hash_senha(senha)
        cursor.execute('''
            SELECT id, nome, email FROM usuarios 
            WHERE email = ? AND senha = ?
        ''', (email, senha_hash))
        
        usuario = cursor.fetchone()
        conn.close()
        
        if usuario:
            # Criar sessão
            session['user_id'] = usuario[0]
            session['user_nome'] = usuario[1]
            session['user_email'] = usuario[2]
            
            return jsonify({
                'sucesso': True, 
                'mensagem': 'Login realizado com sucesso!',
                'usuario': {
                    'id': usuario[0],
                    'nome': usuario[1],
                    'email': usuario[2]
                }
            }), 200
        else:
            return jsonify({'sucesso': False, 'mensagem': 'Email ou senha incorretos'}), 401
            
    except Exception as e:
        return jsonify({'sucesso': False, 'mensagem': f'Erro no servidor: {str(e)}'}), 500

# Rota para verificar se está logado
@app.route('/verificar-sessao', methods=['GET'])
def verificar_sessao():
    if 'user_id' in session:
        return jsonify({
            'logado': True,
            'usuario': {
                'id': session['user_id'],
                'nome': session['user_nome'],
                'email': session['user_email']
            }
        }), 200
    else:
        return jsonify({'logado': False}), 401

# Rota de logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'sucesso': True, 'mensagem': 'Logout realizado com sucesso'}), 200

if __name__ == '__main__':
    init_db()  # Cria o banco de dados ao iniciar
    print('🚀 Servidor iniciado em http://localhost:5000')
    print('📊 Banco de dados criado/conectado com sucesso')
    app.run(debug=True, port=5000)