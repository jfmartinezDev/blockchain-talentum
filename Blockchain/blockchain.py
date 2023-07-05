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
                

# Parte 2: Minado de un bloque de la cadena

