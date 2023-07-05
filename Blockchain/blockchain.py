# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:41:05 2023

@author: Usuario
"""

# Módulo 1: Crear una cadena de bloques
# Instalar Flask: pip install Flask==1.1.2 (Anaconda prompt)

# Importar las librerías
import datetime
import hashlib
import json
from flask import Flask, jsonify
# Parte 1: Crear la cadena de bloques
class Blockchain:
    
    def __init__(self):
        self.chain = [] # Lista donde se guardarán los bloques de la cadena
        self.create_block(proof=1, previous_hash = '0') # Crear bloque genesis
    
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain)+1,
                 'timestamp' : str(datetime.datetime.now()), # Momento exacto del minado del bloque                                     
                 'proof' : proof,
                 'previous_hash' : previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            #Encontrar el valor de new_proof que genera un hash con cuatro ceros a la izquierda
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
                
        return new_proof
    
    #La función hash toma un bloque de la cadena y retorna el hash criptográfico del bloque
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
            
            
                    

# Parte 2: Minado de un bloque de la cadena

# Crear una aplicación web

app = Flask(__name__)

# Crear una Blockchain

blockchain = Blockchain()

# Minar un bloque
@app.route('/mine_block', methods = ['GET'])

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'Felicidades, has minado un nuevo bloque',
                'index': block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash': block['previous_hash'] }
    return jsonify(response), 200


# Obtener la cadena de bloques completa
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain}
                'length' : len(blockchain.chain) }
    return jsonify(response), 200


# Ejecutar App
app.run(host = '0.0.0.0', port = 5000)





