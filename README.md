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
### Les technologies :
- _Python_: Python est un langage de programmation populaire et flexible qui permet de manipuler des données et de créer des modèles de données complexes.
- _Streamlit_: Streamlit est un framework web facile à utiliser pour les développeurs Python qui permet de créer des applications web interactives pour l'analyse de données. Il permet également de visualiser les données et de les présenter de manière esthétique, ce qui le rend parfait pour le développement de l'interface utilisateur.
- _Aylien API_: L'API Aylien est une API de traitement du langage naturel qui permet de réaliser des analyses de sentiment sur les articles de presse. Elle a été choisie pour extraire les données des articles de presse pour ce projet.
- _Kaggle_:Kaggleestuneplateformedecompétitiondedonnéesenlignequiproposedes ensembles de données pour des projets de science des données. L'ensemble de données de prix des voitures a été téléchargé depuis Kaggle pour ce projet.
- _PySpark_ : Bibliothèque open-source de traitement de données distribuées conçue pour être utilisée avec Apache Spark.
- _Kafka_ : Kafka est une plate-forme de diffusion de données distribuée open-source qui permet de transférer des flux de données en temps réel entre des applications ou des systèmes.

## Important : 
Dans le dossier _src_ on trouve : 
- [Analyses_voitures_api.ipynb](https://github.com/LydiaOuam/arch_distribu-/blob/main/src/Analyses_voitures_api.ipynb) --> le script des visualisation fait sur pandas.
- [Streamlit.py](https://github.com/LydiaOuam/arch_distribu-/blob/main/src/Streamlit.py) --> un script qui permet de visualiser les données prevenant de l'API en real Time.
- [apiProducer.py](https://github.com/LydiaOuam/arch_distribu-/blob/main/src/apiProducer.py) --> streamer les données à partir de l'API et cela dans Spark
- [kafkaProducer.py](https://github.com/LydiaOuam/arch_distribu-/blob/main/src/kafkaProducer.py) --> le producer de l'API mais cette fois ci fait hors spark
- [producer.py](https://github.com/LydiaOuam/arch_distribu-/blob/main/src/producer.py) --> Simuler le stream à partir d'un fichier CSV et ecrire dans un Topic
- [consumer3.py](https://github.com/LydiaOuam/arch_distribu-/blob/main/src/consumer3.py) --> Se connecter au topic et passer les données dans le modéle de ML.
- Dossier __testdata3__ qui contient le csv utilisé dans le producer.py
- mymodel.parquet le fichier parquet de modéle ML développé.

Le dossier Data dans lequel y a nos deux datasets mentionné au début
---------------------------------------------------------------
# La Data
---------------------------------------------------------------
Deux Sources de données sont utilisé pour ce projet : 
1. Des données de News concernant des marques spécifiques de voitures collecté en utilisant [l'API Aylien](https://aylien.com)
3. Des données de voiture qui contient plusieurs caractéristique et qu'on a pu récupérer sur [Kaggle](https://www.kaggle.com/datasets/adityadesai13/used-car-dataset-ford-and-mercedes)



---------------------------------------------------------------
# Développement
---------------------------------------------------------------
Pour nous l'objectif était de streamer deux sources de données.
Une étant les données des voitures qu'on a récupérer sur kaggle, en simulant un stream on pourra imaginer une
application derriéres utilisées par des gens et qui remplissent les caracteristique de leurs voitures,
ces caracteristiques seront utilisé dans le
modéle de ML qu'on a développé sur spark et qu'on sauvegarder sous format parquet pour estimer le prix de la voiture.
En deuxiéme on a récuperer des données sur l'API Aylien, car on voulait etudier l'impact des NEWS sur les prix des voitures.
On veut streamer cela et calculer à l'aide des window le nombre de News arrivant pour chaque marque.

---------------------------------------------------------------
# Visualisations
---------------------------------------------------------------
Sur ce graphe on peut voir les cinq types des voitures; Ford, Toyota, Hyundai, Mercedes, Volkswagen, BMW. En appliquant un barplot, la dataframe des news, nous avons ici en vert, les news positif sur chaque marque de voiture qui ont ete publie recemment, en orange nous avons les news neutral, et en bleu les news negatifs.


![type_sentiment](https://user-images.githubusercontent.com/92854230/230239363-e4f3a1e5-121c-4a4b-80eb-af6690eed00a.png)


Dans cette etape, nous allons decouvrir la deuxieme donnee, qui constitue des models et manufacturer des voitures avec leur prix plus d'autre characteristic. 


Cette figure montre les manufacturer des voitures avec les moyens des prix de leurs models, en se basant sur cette dataframe nous pourrons creer la visualisation suivante.

![image](https://user-images.githubusercontent.com/92854230/230239613-da32bcc4-dc02-4a14-9a83-c07ec7c9c54a.png)

Cette visualisation constitue d'un barplot chart des moyens des prix de chaque manufacturer avec leur noms, elle nous montre que en gros la marque Mercedes est la plus chere en se basant sur tous les models, par contre la marque Opel a le prix tres bas.


![barplot_price](https://user-images.githubusercontent.com/92854230/230239433-5398b699-d6dc-487e-b24f-8ee5d209e911.png)


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
    
