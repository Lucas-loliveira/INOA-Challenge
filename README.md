# INOA-Challenge
Autor da solução: Lucas da Silva de Oliveira (lucasoliveira783@gmail.com, https://www.linkedin.com/in/lucas-sil-oliveira)

## Apresentação do problema
O objetivo do sistema é auxiliar um investidor nas suas decisões de comprar/vender ativos. Para tal, ele deve registrar periodicamente a cotação atual de ativos da B3 e também avisar, via e-mail, caso haja oportunidade de negociação.

Os seguintes requisitos funcionais são necessários:

- Obter periodicamente as cotações de alguma fonte pública qualquer e armazená-las, em uma periodicidade configurável (em minutos) para cada túnel, para consulta posterior
- Expor uma interface web para permitir consultar os preços armazenados, configurar os ativos a serem monitorados e parametrizar os túneis de preço de cada ativo e periodicidade da checagem (em minutos) de cada ativo
- Enviar e-mail para o investidor sugerindo Compra sempre que o preço de um ativo monitorado cruzar o seu limite inferior, e sugerindo Venda sempre que o preço de um ativo monitorado cruzar o seu limite superior


## Tecnologias usadas

  * python3
  * django 4.2
  * django-rest framework
  * PostgreSQL
  * Redis
  * Celery
  * Docker-compose\

 
Requisitos
============
  * [docker](https://www.docker.com/)
  * [docker-compose](https://docs.docker.com/compose/)

Como executar a aplicação
============

### Copie as variaveis de ambiente
```bash
$ cp .env-exemple .env
```

### Execute os containers
```bash
$ make build up
```

### Execute as migrações
```bash
$ make migrate
```
### Execute o celery
```bash
$ make celery
```

Testes
=====

```bash
$ make test
```

Documentação (OpenAPI)
=====
http://0.0.0.0:8000/docs/

para os endpoints Stocks notificarion é necessario o JWT, então adicione o token atraves do botão Authorize e adicione o token no formato: 

```bash
$ Bearer *********************
```


Logs de emails enviados
=====
Por default, os emails são mostrados apenas no console, um historico de emails enviados pode ser encontrado no arquivo stock_emails.log

Arquitetura
=====

![inoa drawio](https://github.com/Lucas-loliveira/INOA-Challenge/assets/22778168/4f424c4d-beab-4c57-9813-2ae9aee5d2fa)



A solução está dividida em três módulos principais: User, Stock e Stock Notification.

User: Realiza as operações CRUD dos usuários e gerencia os tokens JWT.

Stock: Utiliza o Celery Beat e o Celery Worker para fazer chamadas periódicas configuráveis no arquivo .env para a API BRAPI. Também é possível visualizar as ações por meio de um endpoint.

Stock Notification: Realiza as operações CRUD das notificações e utiliza um sinal do Django para notificar os usuários por e-mail quando houver uma atualização das ações.

Futuras melhorias
=====
* Melhorar a limitação do Django Signals: A solução proposta utiliza o Django Signals como gatilho para o envio de notificações. No entanto, dependendo da situação, a dependência da atualização das ações para o envio da notificação pode resultar em atrasos na entrega das notificações. Recomenda-se encontrar uma abordagem alternativa para garantir a entrega pontual das notificações, mesmo em casos em que o sistema precise aguardar um intervalo entre notificações. Uma solução seria 

* Adicionar paginação à listagem de Stocks: É importante implementar a funcionalidade de paginação na listagem de ações (Stocks), para evitar a sobrecarga de dados em uma única página. Isso melhorará a usabilidade e a performance do sistema, permitindo que os usuários naveguem pelos resultados de forma mais eficiente.

* Adequação para deploy: Para garantir a segurança e a proteção dos dados, é recomendável adicionar autenticação nos endpoints do módulo User e remover a listagem de tokens JWT. Isso garantirá que apenas usuários autorizados possam acessar esses recursos e protegerá informações sensíveis de autenticação.


