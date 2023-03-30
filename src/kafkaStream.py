import requests
from kafka import KafkaProducer

# Configuration de la connexion Kafka
bootstrap_servers = ['localhost:9092']
topic_name = 'mon-topic'

# Création du producteur Kafka
producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

# Appel de l'API et envoi des données à Kafka

url = 'https://api.worldnewsapi.com/search-news?text=Ford, Mercedes, Volkswagen, bmw, toyota, hyundai'
api_key = '5ab60f9d8cab4f39bddabfc9dd38c452'
source='us, uk'
params = {
    'analyze': True,
    'source-countries': source,
    'api-key': api_key
   
}
while True:
    response = requests.get(url, params=params)
    data = response.json()
    print("mydata : " + data)
   # producer.send(topic_name, str(data).encode('utf-8'))

