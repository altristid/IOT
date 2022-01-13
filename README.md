# IOT
Les différents scripts pour générer et traiter les données
Le script subscriber.py est configuré sur le serveur d'infrastructure, il permet de récupérer les données du broker puis de les insérer dans la base de données

Celui ci envoie des données directement dans la base de données et log dans le fichier : /var/log/Meteosubscriber.log
pour lancer le script : sudo python3 /home/toto/python/subscriber.py

Le script publisher.py est configuré sur le serveur d'objet connecté.
Il log dans le fichier: /var/log/Meteopublisher.log
celui-ci émule les données générés par les capteurs et envoie au broker les données au format json.
pour lancer le script : sudo python3 /home/toto/python/publisher.py
