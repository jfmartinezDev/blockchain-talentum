# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:41:05 2023

@author: Usuario
"""

# Módulo 1: Crear una cadena de bloques
# Instalar Flask: pip install Flask==1.1.2 (Anaconda prompt) 
# pip install Flask --upgrade

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
    #Función para crear los bloques después del minado
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
        # Describir la siguiente línea de código
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            #Verifica la validez de la cadena de bloques verificando si el contenido de la llave previous_hash
            #del bloque actual es igual al hash del bloque previo.
            if block['previous_hash'] != self.hash(previous_block):
                return False
            #Verifica que la prueba de trabajo de todos los bloques de la cadena sea válida. Para esto se emplea
            #la prueba del bloque previo y la prueba del bloque actual para verificar que se supere el algoritmo de
            #encriptación.
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
# Si se obtiene un error 500, actualizar Flask, reiniciar SPYDER y ejecutar la siguiente línea
#app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
# Crear una Blockchain

blockchain = Blockchain()

# Minar un bloque
@app.route('/mine_block', methods = ['GET'])

#Función de minado
def mine_block():
    # Se obtiene el último bloque que ha sido minado
    previous_block = blockchain.get_previous_block()
    # Se obtiene la prueba de trabajo de dicho bloque
    previous_proof = previous_block['proof']
    # Se obtiene la prueba de trabajo del bloque que va a ser minado
    proof = blockchain.proof_of_work(previous_proof)
    #Obtiene el hash del bloque previo para construir el bloque
    previous_hash = blockchain.hash(previous_block)
    #Crea el nuevo bloque empleando la prueba de trabajo y el hash previo
    block = blockchain.create_block(proof, previous_hash)
    #Crea el diccionario de respuesta para la aplicación web
    response = {'message' : 'Felicidades, has minado un nuevo bloque',
                'index': block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash': block['previous_hash'] }
    
    #Convierte a formato JSON el diccionario de respuesta y lo retorna junto con el código de confirmación OK
    return jsonify(response), 200


# Obtener la cadena de bloques completa
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain, # Almacena la cadena de bloques en la llave chain del diccionario de respuesta de la función
                 
                'length' : len(blockchain.chain) } #Almacena la longitud actual de la cadena de bloques
    return jsonify(response), 200 #Convierte a formato JSON el diccionario de respuesta y lo retorna junto con el código de confirmación OK


# Ejecutar App
app.run(host = '0.0.0.0', port = 5000)





