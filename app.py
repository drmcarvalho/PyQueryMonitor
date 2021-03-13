#!/usr/bin/env python
# coding: utf-8

import argparse
import sys
from database import database
from monitor import sqlmonitor, sendDiscord
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


def parserArgs():
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
            default=3306,
            help="Porta utilizada para se conectar no banco, padrão 3306.",
        )
        parser.add_argument(
            "--time",
            default=50,
            help="Especifica o tempo que a query esta executando para que ela possa ser capturada pelo monitor.",
        )
        parser.add_argument(
            "--watch",
            default=5,
            help="O tempo que o monitor vai executar a cada interação para obter as querys",
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
    args = parserArgs()
    connection = database(args.user, args.password, args.host, args.port)
    welcome()
    while True:
        for sm in sqlmonitor(connection, time=args.time):
            if sm:
                viewQuery(sm)
                if args.discord:
                    sendDiscord(formatMenssagem(sm), args.channel, args.token)
        sleep(args.watch)


if __name__ == "__main__":
    main()
