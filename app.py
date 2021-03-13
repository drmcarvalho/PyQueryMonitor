#!/usr/bin/env python
# coding: utf-8

import argparse
import sys
from database import database
from monitor import sqlmonitor
from integration import sendDiscord
from time import sleep


def welcome():
    print(
        """
______      _____                      ___  ___            _ _             
| ___ \    |  _  |                     |  \/  |           (_) |            
| |_/ /   _| | | |_   _  ___ _ __ _   _| .  . | ___  _ __  _| |_ ___  _ __ 
|  __/ | | | | | | | | |/ _ \ '__| | | | |\/| |/ _ \| '_ \| | __/ _ \| '__|
| |  | |_| \ \/' / |_| |  __/ |  | |_| | |  | | (_) | | | | | || (_) | |   
\_|   \__, |\_/\_\\__,_|\___|_|   \__, \_|  |_/\___/|_| |_|_|\__\___/|_|   
       __/ |                       __/ |                                   
      |___/                       |___/                                    
"""
    )


def fatal(error):
    print(error)
    sys.exit(1)


def warning(text):
    print('\033[93m' + text + '\033[0m')


def formatMenssagem(row):
    return "Process id: {id}\nUser: {user}\nHost: {host}\nDB: {db}\nTime: {time}\nState: {state}\nInfo: ```\n{info}\n```".format(
        id=row["ID"],
        user=row["USER"],
        host=row["HOST"],
        db=row["DB"],
        time=row["TIME"],
        state=row["STATE"],
        info=row["INFO"],
    )


def viewQuery(row):
    print(formatMenssagem(row))


def options():
    try:
        parser = argparse.ArgumentParser(
            description="PyQueryMonitor ferramenta para monitoramento de consultas SQL"
        )
        parser.add_argument(
            "--host",
            default="localhost",
            help="Endereço do servidor de banco de dados e o valor padrão é o localhost.",
        )
        parser.add_argument(
            "--user",
            default="root",
            help="Usuário que vai utilizar para fazer o monitoramento, sendo o valor padrão root.",
        )
        parser.add_argument("--password", default="", help="Senha do banco de dados.")
        parser.add_argument(
            "--port",
            type=int,
            default=3306,
            help="Porta utilizada para se conectar no banco, padrão 3306.",
        )
        parser.add_argument(
            "--time",
            default=50,
            type=int,
            help="Especifica o tempo que a query esta executando para que ela possa ser capturada pelo monitor.",
        )
        parser.add_argument(
            "--interval",
            default=5,
            type=int,
            help="O intervalo que o monitor vai executar para obter os processos das consultas que estão demorando. Exemplo: se definir 5 segundos, ele vai verificar os processos das consultadas a cada 5 segundos.",
        )
        parser.add_argument(
            "--discord",
            default=False,
            help="Opção para determinar se vai usar o Discord como log.",
        )
        parser.add_argument("--channel", default=None, help="Id do webhook do Discord.")
        parser.add_argument("--token", default=None, help="Token do canal do webhook do Discord.")
        args = parser.parse_args()
        return args
    except (argparse.ArgumentError, argparse.ArgumentTypeError) as error:
        fatal(error)


def main():
    opt = options()
    connection = database(opt.user, opt.password, opt.host, opt.port)
    welcome()
    while True:
        for sm in sqlmonitor(connection, time=opt.time):
            if not sm:
                continue
            viewQuery(sm)
            if opt.discord:
                ok = sendDiscord(formatMenssagem(sm), opt.channel, opt.token)
                if not ok:
                    warning('Aviso: não foi possível integrar com o discord.')
        sleep(opt.interval)


if __name__ == "__main__":
    main()
