from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, Usuarios
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)

#usuarios = {
#    'eduardo':'1234',
#    'francisquinha':'4321'
#}

#@auth.verify_password
#def verificacao(login, senha):
#    if not (login, senha):
#        return False
#    return usuarios.get(login) == senha

@auth.verify_password
def verificacao(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()
    

class Pessoa(Resource):
    @auth.login_required
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome':pessoa.nome,
                'idade':pessoa.idade,
                'id':pessoa.id
            }
        except AttributeError:
            response = {
                'status':'Error',
                'mensagem':'Nome inexistente, verifique se foi digitado corretamente.'
            }
        return response

    @auth.login_required
    def post(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            dados = request.json
            if 'nome' in dados:
                pessoa.nome = dados['nome']
            if 'idade' in dados:
                pessoa.idade = dados['idade']
            pessoa.save()
            response = {
                'id':pessoa.id,
                'nome':pessoa.nome,
                'idade':pessoa.idade
            }
        except AttributeError:
            response = {
                'status':'Error',
                'mensagem':'Nome inexistente, verifique se foi digitado corretamente.'
            }
        return response
    
    @auth.login_required
    def delete(self, nome):
        pessoa = pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            pessoa.delete()
            response = {'status':'Sucesso', 'mensagem':'Pessoa excluída com sucesso'}
        except AttributeError:
            response = {'status':'Erro', 'mensagem':'Pessoa não encontrada'}
        return response
    
class ListarPessoas(Resource):
    @auth.login_required
    def get(self):
        pessoas = Pessoas.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'idade':i.idade} for i in pessoas]
        return response
    
    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id':pessoa.id,
            'nome':pessoa.nome,
            'idade':pessoa.idade
        }
        return response

class ListaAtividades(Resource):
    @auth.login_required
    def get(self):
        atividades = Atividades.query.all()
        response = [{'id':i.id, 'nome':i.nome, 'pessoa':i.pessoa.nome} for i in atividades]
        return response

    @auth.login_required
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(nome=dados['nome'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa':atividade.pessoa.nome,
            'nome':atividade.nome,
            'id':atividade.id
        }
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>')
api.add_resource(ListarPessoas, '/pessoa')
api.add_resource(ListaAtividades, '/atividades')

if __name__ == '__main__':
    app.run(port=80, debug=True)