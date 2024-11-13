import sqlite3
import re

def get_number(text:str):
    content_lines = text.split("\n")
    numbers_name = re.compile('[0-9]*')
    name = ""
    for x in range(len(content_lines)):
        if content_lines[x].rstrip() == "**nombre":
            name = content_lines[x+1]
            break
    matches = numbers_name.match(name)
    if matches[0] == "":
        print("no number detected") 
    number = int(matches[0]) 
    return number

def get_name(text:str):
    content_lines = text.split("\n")
    name = ""
    for x in range(len(content_lines)):
        if content_lines[x].rstrip() == "**nombre":
            name = content_lines[x+1]
            break
    name = re.sub(r'[0-9]*\.',"", name)
    name.lstrip()
    return name

def get_coro(text:str):
    content_lines = text.split("\n")
    coro = ""
    coro_detected = False
    for x in range(len(content_lines)):
        if content_lines[x].rstrip() == "**fin CORO":
            coro_detected = False
            break

        if coro_detected:
            coro += content_lines[x] + "\n"

        if content_lines[x].rstrip() == "**CORO":
            coro_detected = True

    coro = coro.rstrip("\n")
    return coro

def get_estrofa(text:str):
    content_lines = text.split("\n")
    estrofa = ""
    estrofa_detected = False
    estrofas_array = []
    for x in range(len(content_lines)):
        if content_lines[x].rstrip() == "**fin estrofa":
            estrofa_detected = False
            estrofa = estrofa.rstrip("\n")
            estrofas_array.append(estrofa)
            estrofa = ""

        if estrofa_detected:
            estrofa += content_lines[x] + "\n"

        if content_lines[x].rstrip() == "**estrofa":
            estrofa_detected = True
    return estrofas_array 

def get_cita(text:str):
    content_lines = text.split("\n")
    cita = ""
    for x in range(len(content_lines)):
        if content_lines[x].rstrip() == "**cita":
            cita = content_lines[x+1]
            break
    return cita

def save_alabanza(id:int, nombre:str, cita:str, coro:str):
    try: 
        conn = sqlite3.connect("dbAlabanzas.db")
        cur = conn.cursor()
        data = (id, nombre, cita , coro)
        cur.execute('INSERT INTO Alabanza(id_alabanza, nombre, cita, coro) VALUES (?,?,?,?);', data)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        raise e

def save_estrofa(id:int, estrofas:[]):
    try:
        conn = sqlite3.connect("dbAlabanzas.db")
        cur = conn.cursor()
        for x in range(len(estrofas)):
            data = (id, x+1, estrofas[x])
            cur.execute('INSERT INTO Estrofa(alabanza_id,estrofa, numero_estrofa) VALUES (?,?,?);', data)
            conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        raise e

f = open("contentPrueba.txt", "r")
content_read = f.read()

split_content = content_read.split("------------------------------------------")

print("cargando "+ str(len(split_content)) + " alabanzas")

for x in split_content:
    print(".....")
    number_alabanza = get_number(x)
    name_alabanza = get_name(x)
    cita_alabanza = get_cita(x)
    coro_alabanza = get_coro(x)
    estrofa_alabanza = get_estrofa(x)
    save_alabanza(number_alabanza, name_alabanza,cita_alabanza, coro_alabanza)
    save_estrofa(number_alabanza, estrofa_alabanza)

print("carga finalizada con exito")
