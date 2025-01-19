import pymongo
import pytz
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import json
import random
import math
from typing import Optional, Union, Tuple, Any

connection_string = 'mongodb+srv://victorsouzalith98:Fk3j85smXfWrUdSk@cluster0economisty.zwntl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0Economisty'
sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
dados_evento_moedas = {}

async def find_db_collection(collection_name: str):
    client = AsyncIOMotorClient(connection_string)
    db = client['economisty']
    db_collection = db[collection_name]
    return db_collection

async def checar_cooldown(user_id: int) -> bool:
    db_collection = await find_db_collection('users')
    filtro = {"user_id": user_id}

    registro = await db_collection.find_one(filtro, {"cooldown": 1, "_id": 0})
    data_registro = str(registro.get("cooldown"))
    data_de_hoje = str(datetime.now(sao_paulo_tz).date())

    if data_registro == data_de_hoje:
        return True
    else:
        return False

async def atualizar_cooldown(user_id: int) -> None:
    db_collection = await find_db_collection('users')
    filtro = {"user_id": user_id}
    data_de_hoje = str(datetime.now(sao_paulo_tz).date())
    await db_collection.update_one(filtro, {"$set": {"cooldown": data_de_hoje}})

async def reset_cooldown(user_id: int) -> None:
    db_collection = await find_db_collection('users')
    filtro = {"user_id": user_id}
    await db_collection.update_one(filtro, {"$set": {"cooldown": None}})

def carregar_eventos_moedas():
    global dados_evento_moedas
    with open('repositorio/economisty/eventos.json', "r", encoding="utf-8") as arquivo:
        dados_evento_moedas = json.load(arquivo)

async def evento_moedas(salario: int, exp: int, user_id: int) -> [int, int, [dict, None], bool]:
    pesos = [evento["peso"] for evento in dados_evento_moedas]
    evento = random.choices(dados_evento_moedas, weights=pesos, k=1)[0]

    # Mapeamento para tratamento dos eventos
    evento_handlers = {
        "adicionar_moedas": lambda s, e: (s + evento["modificador"], e),
        "subtrair_moedas": lambda s, e: (s - evento["modificador"], e),
        "multiplicador_moedas_e_exp": lambda s, e: (s * evento["modificador"], e * evento["modificador"]),
        "adicionar_exp": lambda s, e: (s, e + evento["modificador"]),
        "subtrair_e_multiplicar_moedas_e_exp": lambda s, e:(s - evento["modificador"]["moedas"], e * evento["modificador"]["exp"]),
        "subtrair_percentual_moedas": lambda s, e: (int(s * (evento["modificador"] / 100)), e),
        "subtrair_exp": lambda s, e: (s, e - evento["modificador"])
    }

    if evento["tipo_evento"] == "time_reset":
        await reset_cooldown(user_id)
        return salario, exp, evento, True

    # Processa o evento se houver um handler correspondente
    handler = evento_handlers.get(evento["tipo_evento"])
    if handler:
        salario, exp = handler(salario, exp)
        return salario, exp, evento, True

    # Retorna padrão caso não encontre o tipo de evento
    return salario, exp, None, False

async def buscar_usuario(user_id: int):
    db_collection = await find_db_collection('users')
    data_user = await db_collection.find_one({"user_id": user_id})
    return data_user

async def alterar_saldo(user_id: int, quantidade: int) -> None:
    db_collection = await find_db_collection('users')
    filtro = {"user_id": user_id}
    await db_collection.update_one(filtro, {"$inc": {"saldo_moedas": quantidade}})

def calcular_exp_para_proximo_nivel(nivel_atual: int, a=300, b=100) -> int:
    return int(a * math.log(nivel_atual) + b)

def cargo_por_level(level: int) -> [dict, None]:
    cargo = {
        range(20, 40): {"role": "Assistente", "salario": 1000},
        range(40, 60): {"role": "Analista", "salario": 1500},
        range(60, 80): {"role": "Coordenador", "salario": 2000},
        range(80, 100): {"role": "Gerente", "salario": 2500},
        range(100, 999): {"role": "Diretor", "salario": 3000}
    }

    for intervalo, cargo in cargo.items():
        if level in intervalo:
            return cargo
    return None

async def adicionar_exp(user_id, exp_gain: int=0) -> tuple[Any, Any | None] | None:
    collection = await find_db_collection('users')
    filtro = {"user_id": user_id}

    dados_usuario = await collection.find_one(filtro)
    nivel_atual = dados_usuario["level"]

    boost_exp = await checar_vale_exp(user_id)

    new_exp = int(dados_usuario["exp"] + (exp_gain * boost_exp))
    new_total_exp = int(dados_usuario["total_exp"] + (exp_gain * boost_exp))

    while new_exp >= calcular_exp_para_proximo_nivel(nivel_atual):
        new_exp -= calcular_exp_para_proximo_nivel(nivel_atual)
        nivel_atual +=1

    new_cargo = cargo_por_level(nivel_atual)

    if new_cargo is None:
        await collection.update_one(filtro,
                                        {"$set": {"exp": new_exp, "level": nivel_atual, "total_exp": new_total_exp}})
    else:
        await collection.update_one(filtro,
                                        {"$set": {"exp": new_exp, "level": nivel_atual, "total_exp": new_total_exp, "cargo": new_cargo}})

    if nivel_atual > dados_usuario["level"]:
        return nivel_atual, new_cargo
    else:
        return None

async def checar_vale_exp(user_id: int) -> float:
    db_collection = await find_db_collection('users')
    filtro = {"user_id": user_id}

    user_data = await db_collection.find_one(filtro)

    data_atual = datetime.now()
    boost_multiplier = 1.0
    if user_data["boost_exp"]["expires_at"]:
        expires_at = user_data["boost_exp"]["expires_at"]
        if data_atual < expires_at:
            boost_multiplier = user_data["boost_exp"]["boost_multiplier"]
        else:
            await db_collection.update_one(filtro, {"$set": {"boost_exp.boost_multiplier": None, "boost_exp.expires_at": None}})

    return boost_multiplier

async def rank_de_usuarios() -> list:
    db_collection = await find_db_collection('users')
    data_users = await db_collection.find({"total_exp": {"$gt": 0}}).sort("total_exp", pymongo.DESCENDING).to_list(length=None)
    return data_users
