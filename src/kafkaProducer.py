# Producer sans spark

import requests
import json
import time
from kafka import KafkaProducer
from datetime import datetime
from json import dumps

if __name__ == "__main__":
    
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x: dumps(x).encode('utf-8'),
                             api_version=(2,0,2))
    
    # Define the API endpoint URL
    url = 'https://api.aylien.com/news/stories'

    # Define the initial payload parameters
    type_param = 'Ford'  # Replace with your desired query
    payload = {
        'aql': f'text:({type_param}) AND language:en',
        'published_at.start': 'NOW-365DAYS/DAY',
        'published_at.end': 'NOW',
        'sort_by': 'published_at',
        'sort_direction': 'desc',
        'cursor': '*',
        'per_page': 100
    }

    headers = {
        'X-Application-ID': 'acec876a',
        'X-Application-Key': '419ececeb9d87be8607f81a9e05bbd9f'
    }
    id_counter = 0
    
    # Send data to Kafka topic every 5 seconds
    while True:
        # Fetch the data from the API
        response = requests.get(url, headers=headers, params=payload)
        data = response.json()
        id_counter += 1
        
        # Extract the desired fields from the API response
        extracted_data = []
        for article in data['stories']:
            extracted_article = {
                'type': type_param,
                'id': article['id'],
                'sentiment_body_p': article['sentiment']['body']['polarity'],
                'sentiment_body_s': article['sentiment']['body']['score'],
                'sentiment_title_p': article['sentiment']['title']['polarity'],
                'sentiment_title_s': article['sentiment']['title']['score'],
                'published': article['published_at']
            }
            extracted_data.append(extracted_article)
            

        print("send NÂ°: ", id_counter)
        producer.send('Hello-Kafka', value=extracted_data)
        print(extracted_data)
        time.sleep(2)