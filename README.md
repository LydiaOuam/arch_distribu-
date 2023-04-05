# Projet Architecture Distribué (Kafka Stream)

---------------------------------------------------------------
# La description du projet
---------------------------------------------------------------
Ce projet est réalisé dans le cadre du TP noté du module Architecture Distribué.
Le but de ce projet est d'utiliser kafka pour manipuler des données qui provient de différentes sources en Streaming.
Comprendre la force de Kafka qui réside dans le fait que cet outil peut ingérer des données réels qui provient de différentes sources.
Traiter ces données en temps réel et cela en utilisant SparkStreaming par exemple, aussi diffuser ces données.
Un autre point fort de cet outil c'est qu'il permet d'utiliser la notion des Windows pour aggréger les données en utilisant des intervalles de temps débutant de l'ordre des millisecondes.

---------------------------------------------------------------
# Ce qui faut savoir
---------------------------------------------------------------
Les Kafkas messages sont toujours un couple de {key, value}.
Plusieurs producers et consumers et topics peuvent utilisent dans un seul processus de stream.
Les producers récupere la données et la mettent dans les topics sous forme de message, les consumers s'inscrivent aux topics et récupére les données.

Pour notre Cas on a créer un docker compose qui est constitué de kafka, zookeeper, spark, deux worker. Deux volumes partagés entre les différents container.
Nos Script sont sauvegardés dans le volume paratgé src. Pour lancer un script pyspark faut rentrer dans l'image docker et exécuter cette commande dans le bin  :
```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 pathFile
```

---------------------------------------------------------------
# La Data
---------------------------------------------------------------
Deux Sources de données sont utilisé pour ce projet : 
1. Des données de News concernant des marques spécifiques de voitures collecté en utilisant [l'API Aylien](https://aylien.com)
3. Des données de voiture qui contient plusieurs caractéristique et qu'on a pu récupérer sur [Kaggle](https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes).

---------------------------------------------------------------
# Développement
---------------------------------------------------------------
Pour nous l'objectif était de streamer deux sources de données.
Une étant les données des voitures qu'on a récupérer sur kaggle, en simulant un stream on pourra imaginer une application derriéres utilisées par des gens et qui remplissent les caracteristique de leurs voitures, ces caracteristiques seront utilisé dans le modée de ML qu'on a développé sur spark et qu'on sauvegarder sous format parquet

---------------------------------------------------------------
# Visualisations
---------------------------------------------------------------
Sur ce graphe on peut voir en orange les prix des bitcoins et en bleu le nombre de tweets, on peut remarquer que l'augmentation des prix des bitcoins suit la hausse des nombre des tweets.

Faut aussi savoir que les prix des cryptos sont influencé par plusieurs autre éléments comme : l'offre et la demande, incertitudes politiques et économiques, ...

<img width="900" alt="Capture d’écran 2023-01-20 à 12 08 36" src="https://user-images.githubusercontent.com/84903904/214848632-d64eae7d-e3ac-4a26-9d20-46c9c74798e2.png">

Cette Image on peut voir l'évolution de prix de 4 différentes cryptos. 

<img width="900" alt="Capture d’écran 2023-01-20 à 12 08 36" src="https://user-images.githubusercontent.com/84903904/214862466-56445bb0-713f-4b3a-90d9-d476e962db6d.png">



Cette figure montre un _treemap_ composé de trois couches la premiére représente le nom de la crypto, la deuxiéme est l'heure et la troisiéme c'est le prix, les informations qu'on voit sur le _treemap_ sont les données des derniéres 24H.

<img width="835" alt="Capture d’écran 2023-01-26 à 14 56 34" src="https://user-images.githubusercontent.com/84903904/214854013-728054cf-a773-42a6-b906-1278ab07d4fe.png">


---------------------------------------------------------------
# Difficultés
---------------------------------------------------------------

Face à un contexte complétement nouveau pour nous, et aussi le manque de ressources existante sur internet, on a remarqué qu'on passe beaucoup de temps à chercher à comprendre le fonctionnement des choses, et donc par conséquent peu de temps productif en concrét.
Le cours est trés intéressant mais trés vaste. 
Le Choix du sujet.

---------------------------------------------------------------
# Collaborateurs
---------------------------------------------------------------
    Lydia 
    Kafia 
    Boutaina 
    
