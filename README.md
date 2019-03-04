# weather project
Utilizando python com o microframework Flask esse projeto contém um único Endpoint que em um GET request passando como parâmetros uma data de ínicio, uma data final(as quais não podem serem maior que 7 dias do dia de hoje) e o código de uma cidade retorna em JSON contendo nesse intervalo de datas qual o dia com previsão de maior temperatura, menor temperatura e de mais chuva, consumindo da API do climatempo(https://advisor.climatempo.com.br/).

# setup
1 - Criar uma Virtualenv
```
python3 -m venv venv
```
2 - Ativar a venv
```
source ./venv/bin/activate
```
3 - Instalar requirements

dentro da pasta weather_project fazer o comando:
```
pip install -r requirements.txt
```
4 - Configurar banco de dados

dentro da pasta weather_project realizar os seguintes comandos:
```
python manage.py db init
```
```
python manage.py db migrate
```
```
python manage.py db upgrade
```
5 - Exportar o seu token do climatempo

Faça login no site da climatempo https://advisor.climatempo.com.br/login

clique em tokens no canto superior esquerdo

crie um novo projeto e gere um token

exporte o token no seu ambiente da seguinte maneira:

```
export CLIMATEMPO_TOKEN="your_token"
```
6 - Agora é só rodar o projeto:
```
python manage.py runserver
```

# exemplo de requisição
a requisição devera ser passada da seguinte maneira:

```
http://127.0.0.1:5000/api/v1/weather?city_code=city_code&from_date=from_date&to_date=to_date"
```
lembrando que o city_code vc consegue através da api do climatempo(http://apiadvisor.climatempo.com.br/doc/index.html#api-Locale-GetCityByNameAndState), o formato da data deve ser YYYY-MM-DD, a data de inicio tem que ser antes da do final e não poderá passar 7 dias do dia atual.

a requisição montada ficara assim:
```
curl -i "http://127.0.0.1:5000/api/v1/weather?city_code=3477&from_date=2019-03-04&to_date=2019-03-10"
```
aonde 3477 é o ID da cidade de São Paulo, 2019-03-04(Quatro de Março de 2019) a data de ínicio e 2019-03-10(Dez de Março de 2019) a data final. 

# exemplo de resposta
a resposta vem da seguinte maneira:
```
{  
   "max_rain":{  
      "day":"2019-03-04",
      "value":"13"
   },
   "max_temp":{  
      "day":"2019-03-05",
      "value":31
   },
   "min_temp":{  
      "day":"2019-03-04",
      "value":18
   }
}
```

aonde max_rain é sobre a previsão de chuva mostrando o dia com maior previsão e o valor esperado de chuva em mm,
min_temp é sobre a previsão de temperatura máxima mostrando o dia com previsão de maior temperatura e o valor da temperatura em graus celsius e min_temp é sobre a previsão de temperatura mínima mostrando o dia com previsão de menor temperatura e o valor da temperatura em graus celsius.

