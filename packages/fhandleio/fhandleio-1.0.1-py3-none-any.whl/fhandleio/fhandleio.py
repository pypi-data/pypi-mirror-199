##################
#
# FIO LIBRARY: SIMPLE EASY HANDLING
#
##################

import json
import os
import pickle
import base64

def check_file(file_name):
    try:
        if os.path.exists(file_name):
            return True
        else:
            return False
    except:
        return "Error"

def read(file_name):
    try:
        with open(file_name, "r") as f:
            return f.read()
        
    except:
        if check_file(file_name):
            return "Error could not be found"
        else:
            return "File does not exist"
        
def readb(file_name):
    try:
        with open(file_name, "rb") as f:
            return f.read()
        
    except:
        if check_file(file_name):
            return "Error could not be found"
        else:
            return "File does not exist"
        
def readl(file_name, x=1):
    try:
        with open(file_name, "r") as f:
            return f.readline(x)
        
    except:
        if check_file(file_name):
            return "Error could not be found"
        else:
            return "File does not exist"
        
def readls(file_name):
    try:
        with open(file_name, "r") as f:
            return f.readlines()
        
    except:
        if check_file(file_name):
            return "Error could not be found"
        else:
            return "File does not exist"
        

def write(file_name, message: str):
    try:
        with open(file_name, "w") as f:
            f.write(message)
        
    except:
        print("ERROR")

def writeb(file_name, data):
    try:
        with open(file_name, "wb") as f:
            f.write(data)
        
    except:
        print("ERROR")
    
def writels(file_name, message: str):
    try:
        with open(file_name, "w") as f:
            f.writelines(message)
            
        
    except:
        print("ERROR")

def append(file_name, data):
    try:
        with open(file_name, "a") as f:
            f.write(data)
            
        
    except:
        print("ERROR")

def appendb(file_name, data):
    try:
        with open(file_name, "ab") as f:
            f.write(data)
            
        
    except:
        print("ERROR")

def create(file_name):
    # Creates error if doesn'already exists exist
    with open(file_name, 'x') as f:
        pass
    
def trunc(file_name, bytes: int):
    try:
        with open(file_name, "w") as f:
            f.truncate(bytes)
            

    except:
        print("Error")

def fileno(file_name):
    try:
        with open(file_name, "wb") as f:
            return f.fileno()

    except:
        return "Error"

def seek_and_tell(file_name, *index):
    try:
        with open(file_name, "r") as f:
            f.seek(index)
            f.tell()
            return f.readline()
    except:
        return "Error"
    
def raw(file_name):
    try:
        with open(file_name, "r") as f:
            return f
    except:
        return "Error"
    
def is_empty(file_name):
    try:
        with open(file_name, "r") as f:
            if f.read(1):
                return False
            else:
                return True
    except:
        return "Error"
    
def chunk_read(file_name, byte):
    try:
        with open(file_name, "r") as f:
            data = f.read(byte)
            return data
    except:
        return "Error"
    
def get_size(file_name):
    try:
        return os.path.getsize(file_name)
    except FileNotFoundError:
        return "FileNotFound"

            

def save_data(filename, data, override=True, hashing=False, mode="txt"):
    # Modes: To txt, py, pickle, json
    # Hashing: Base64
    if mode=="txt":
        if override:
            with open(f"{filename}.txt", "w") as f:
                if hashing:
                    try:
                        data = base64.b64encode(data)
                    except:
                        pass
                f.write(data)
        else:
            with open(f"{filename}.txt", "a") as f:
                if hashing:
                    try:
                        data = base64.b64encode(data)
                    except:
                        pass
                f.write(data)

    elif mode=="py":
        if override:
            with open(f"{filename}.py", "w") as f:
                if hashing:
                    try:
                        data = base64.b64encode(data)
                    except:
                        pass
                f.write(data)
        else:
            with open(f"{filename}.py", "a") as f:
                if hashing:
                    try:
                        data = base64.b64encode(data)
                    except:
                        pass
                f.write(data)

    elif mode=="pickle":
        if override:
            with open(f'{filename}.pickle', 'wb') as h:
                if hashing:
                    try:
                        data = base64.b64encode(data)
                    except:
                        pass
                pickle.dump(data, h, protocol=pickle.HIGHEST_PROTOCOL)

        else:
            with open(f'{filename}.pickle', 'ab') as h:
                if hashing:
                    try:
                        data = base64.b64encode(data)
                    except:
                        pass
                pickle.dump(data, h, protocol=pickle.HIGHEST_PROTOCOL)

    elif mode=="json":
        if override:
            with open(f'{filename}.txt', "wb") as j:
                if hashing:
                    try:
                        data = base64.b64encode(data)
                    except:
                        pass
                json.dump(data, j)

        else:
            with open(f'{filename}.txt', "ab") as j:
                if hashing:
                    try:
                        data = base64.b64encode(data)
                    except:
                        pass
                json.dump(data, j)


    
        

def load_data(filename, hashed=False, mode="txt"):
    # Modes: To txt, py, pickle, json, excel, sqlite3, sqldict
    if mode=="json":
        with open(f'{filename}.txt') as j:
            data = json.load(j)
            if hashed:
                data = base64.b64decode(data)
            return data
        
    elif mode=="txt":
        with open(f'{filename}.txt') as f:
            data = f.readlines()
            if hashed:
                data = base64.b64decode(data)
            return data
        
    elif mode=="pickle":
        with open(f'{filename}.pickle', 'rb') as h:
            data = pickle.load(h)
            if hashed:
                data = base64.b64decode(data)
            return data
    

    elif mode=="py":
        with open(f'{filename}.py', 'rb') as f:
            data = f.readlines()
            if hashed:
                data = base64.b64decode(data)
            return data






    
