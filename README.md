# BlockChain Project

Ce projet contient deux implémentations deux blockchain différentes réalisées dans deux langages :

* Python (3.6)
* Java (1.8)

Ces deux implémentations ont un objectif purement pédagogique, et ne sont donc pas prêtes à être déployées
en production.

Ce projet a été réalisé dans le cadre du cours de système réparti durant le semestre d'été 2018 à l'UQAC.
Il est étroitement lié au rapport écrit.

## Blockchain en Java

La version en Java est une version complète de ce que peut être un noeud sur la blockchain. Cette version contient
les fonctionnalités suivantes :

* Gestion de Wallet en local
* Gestion des transactions locales
* Identification par clé publique et privée
* Vérification de l'intégrité de la blockchain
* Minage d'un bloc pour l'ajouter à la chaîne

Cette version n'est cependant pas utilisable par plusieurs noeuds en réseau, elle n'est que sur un seule noeud local.

## Blockchain en Python

La version en Python reprend la majeure partie des fonctionnalités de la version Java en y ajoutant la partie réseau
en REST (http) :

* Gestion des transactions en réseaux entre plusieurs noeuds
* Vérification de l'intégrité de la blockchain
* Minage d'un bloc pour l'ajouter à la chaîne
* Ajout d'un nouveau noeud au réseau
* Algoritme de gestion des conflits, consensus, entre les différents noeuds

Cette blockchain est très proche d'une application réelle, puisque les noeuds mine constament des nouveaux blocks. Il
y a établissement d'un consensus entre les différents noeuds pour garder la blockchain synchronisé. On peut aussi y 
éffectuer des transactions en utilisant les requêtes http.

## Langages de développement

* Python3.6
* Java
* Htttp
* Json

## Framework & Outils utilisés

Liste non exhaustive des outils et Frameworks utilisés pour la version **JAVA** :

* [InteliJ](https://www.jetbrains.com/idea/) - IDE java utilisé
* [Gson Builder](https://google.github.io/gson/apidocs/com/google/gson/GsonBuilder.html) - API Google Json pour java
* [Java Security](https://docs.oracle.com/javase/7/docs/api/java/security/package-summary.html) - API java security

Liste non exhaustive des outils et Frameworks utilisés pour la version **PYTHON** :

* [PyCharm](https://www.jetbrains.com/pycharm/) - IDE python utilisé
* [Flask](http://flask.pocoo.org/) - Library python pour supporter les requêtes REST (Http)
* [Postman](https://www.getpostman.com/) - Execution des requêtes Http sur l'api python développé

## Authors

* **Cros Camille** - [xkr0 GitHub](https://github.com/xKr0)
* **Pera Vincent** - [Vincent Pera GitHub](https://github.com/VincentPera)
* **Corfa Sébastien** - [Sebspas GitHub](https://github.com/sebspas)
