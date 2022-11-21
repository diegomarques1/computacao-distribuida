# Diego Souza Lima Marques - TIA: 32039921
# Lucas de Camargo Gonçalves - TIA: 32074964
# Laboratório 07 - Banco Distribuído com Webservices

from flask import Flask, jsonify, request, render_template
#from flask_mysqldb import MySQL
from datetime import datetime
import uuid
import socket

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#app.config['MYSQL_HOST'] = 'database-lab07.carqgrxaslmw.us-east-1.rds.amazonaws.com'
#app.config['MYSQL_USER'] = 'admin'
#app.config['MYSQL_PASSWORD'] = 'admin123'
#app.config['MYSQL_DB'] = 'flask'
#mysql = MySQL(app)

acnt_list = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
num_op = 0
token_list = []

arquivo = open("log.txt", "w")
arquivo.write("TIMESTAMP, NumOperação, IP Servidor Negócio, TipoOperação, Conta1, [Conta2], Valor\n")
arquivo.close()

def validarToken(header):
    if header not in token_list:
        return "Token inválido"
    return "Token válido"

@app.route('/deposito/<int:acnt>/<int:amt>',methods=['POST'])
def realizarDeposito(acnt, amt):
    if validarToken(request.headers["token"]) == "Token inválido":
        return "Operação não autorizada",403

    acnt_list[acnt - 1] += amt
    global num_op
    num_op += 1
        
    arquivo = open("log.txt", "a")
    arquivo.write("{}, {}, {}, {}, {}, {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),num_op,socket.gethostbyname(socket.gethostname()),"deposito",acnt,amt))
    arquivo.close()
        
    return "Depósito de {} reais realizado!".format(amt),200
    

@app.route('/saque/<int:acnt>/<int:amt>',methods=['DELETE'])
def realizarSaque(acnt, amt):
    if validarToken(request.headers["token"]) == "Token inválido":
        return "Operação não autorizada",403
    
    if acnt_list[acnt - 1] < amt:
        return "Erro -> Valor do saque é maior que o valor na conta"

    acnt_list[acnt - 1] -= amt
    global num_op
    num_op += 1
    
    arquivo = open("log.txt", "a")
    arquivo.write("{}, {}, {}, {}, {}, {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),num_op,socket.gethostbyname(socket.gethostname()),"saque",acnt,amt))
    arquivo.close()
    
    return "Saque de {} reais realizado!".format(amt),200

@app.route('/saldo/<int:acnt>',methods=['GET'])
def getSaldo(acnt):
    if validarToken(request.headers["token"]) == "Token inválido":
        return "Operação não autorizada",403
    
    global num_op
    num_op += 1

    arquivo = open("log.txt", "a")
    arquivo.write("{}, {}, {}, {}, {}, {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),num_op,socket.gethostbyname(socket.gethostname()),"saldo",acnt,acnt_list[acnt - 1]))
    arquivo.close()
    
    return jsonify(acnt_list[acnt - 1]),200

@app.route('/transferencia/<int:acnt_orig>/<int:acnt_dest>/<int:valor>',methods=['PATCH'])
def realizarTransferencia(acnt_orig, acnt_dest, valor):
    if validarToken(request.headers["token"]) == "Token inválido":
        return "Operação não autorizada",403
    
    if acnt_list[acnt_orig - 1] < valor:
        return "Erro -> Valor da transferência é maior que o valor da conta de origem"

    acnt_list[acnt_orig - 1] -= valor
    acnt_list[acnt_dest - 1] += valor
    global num_op
    num_op += 1

    arquivo = open("log.txt", "a")
    arquivo.write("{}, {}, {}, {}, {}, {}, {}\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"),num_op,socket.gethostbyname(socket.gethostname()),"transferencia",acnt_orig,acnt_dest,valor))
    arquivo.close()
    
    return "Transferência de {} para {} de {} reais realizada!".format(acnt_orig, acnt_dest, valor),200

@app.route('/auth',methods=['GET'])
def autenticar():
    my_id = uuid.uuid4()
    token_list.append(str(my_id))
    return jsonify(my_id),200

@app.route('/',methods=['GET'])
def home():
    return "<h1>Lab07</h1><h2>Diego Souza Lima Marques - TIA: 32039921</h2><h2>Lucas de Camargo Gonçalves - TIA: 32074964</h2>"
    
if __name__ == '__main__':
    app.run()
