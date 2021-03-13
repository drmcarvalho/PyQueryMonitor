# PyQueryMonitor
Ferramento para monitoramento de consultas lentas em SQL

# Instalação

Clone o repositório para sua maquina:

`git clone https://github.com/drmcarvalho/PyQueryMonitor.git`

Acesse o diretorio do repositorio clonado:

`cd PyQueryMonitor`

Crie e ative seu ambiente virtual (virtualenv) e em seguida instale as depedencias executando o seguinte comando:

`pip install -r requirements.txt`

Após ter seguido esses passos a ferramenta vai estar pronta para uso.

---

# Executando

Para executar o PyQueryMonitor você pode começar vendo as opções disponivel executando o seguinte comando:

`python app.py --help`

Opções:

```
usage: app.py [-h] [--host HOST] [--user USER] [--password PASSWORD]
              [--port PORT] [--time TIME] [--watch WATCH] [--discord DISCORD]
              [--channel CHANNEL] [--token TOKEN]

PyQueryMonitor ferramenta para monitoramento de consultas SQL

optional arguments:
  -h, --help           show this help message and exit
  --host HOST          Endereço do servidor de banco de dados e o valor padrão
                       é o localhost.
  --user USER          Usuário que vai utilizar para fazer o monitoramento,
                       sendo o valor padrão root.
  --password PASSWORD  Senha do banco de dados.
  --port PORT          Porta utilizada para se conectar no banco, padrão 3306.
  --time TIME          Especifica o tempo que a query esta executando para que
                       ela possa ser capturada pelo monitor.
  --watch WATCH        O tempo que o monitor vai executar a cada interação
                       para obter as querys
  --discord DISCORD    Opção para determinar se vai usar o Discord como log.
  --channel CHANNEL    Id do webhook do Discord.
  --token TOKEN        Token do canal do webhook do Discord.
```

## Iniciando um monitoramento

Vamos começar com um monitoramento basico:

`python app.py --user root --password minha_senha`

Você também pode especificar servidores remotos utilizando a opção `host` para monitorar. Segue um exemplo de saída:

```
Process id: 12345678
User: user
Host: 127.0.0.1:0000
DB: database
Time: 10
State: Sending data
Info:
SELECT conteudo FROM posts WHERE autor like '%fulano%'
```

A ferramenta possui integração com webhook do Discord.

