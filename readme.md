Projet Gestion Imprimantes, Réservations et Filaments
Module 164 – 08.06.2025

Mon projet consiste en une interface web réalisée avec HTML, Flask, Python et une base de données MySQL.

Ce projet permet d’afficher et de gérer les données de cinq tables principales :
Imprimante, Personne, Filament, Fichiers Utilisables, et Réservation.

Fonctionnalités principales
Page Imprimante
Permet d’afficher la liste des imprimantes, ainsi que d’ajouter, modifier et supprimer des imprimantes.

Page Personne
Affiche la liste des personnes, avec la possibilité d’ajouter et de supprimer des personnes.

Page Filament
Sert uniquement à consulter les informations sur les filaments. Aucune modification n’est possible depuis l’interface.

Page Fichiers Utilisables
Permet de consulter les fichiers disponibles pour impression. Elle peut être en lecture seule ou modifiable selon l’évolution du projet.

Page Réservation
Affiche toutes les réservations faites pour les imprimantes. Elle permet d’en créer de nouvelles, et potentiellement d’en modifier ou supprimer.

Chaque page est adaptée aux besoins spécifiques du CRUD (Create, Read, Update, Delete), en fonction du type de données concerné.

Prérequis pour faire fonctionner le projet
Un serveur MySQL doit être installé et actif. Exemples :

LARAGON (avec HeidiSQL)

XAMPP

UWAMP

MAMP (pour Mac)

Python doit être installé sur la machine.
➤ Important : cocher l’option “Add Python to PATH” lors de l’installation.

Git doit être installé : https://gitforwindows.org

Configuration recommandée
Utiliser PyCharm Community Edition comme environnement de développement (IDE).

Lors de l'installation de PyCharm :

Cochez les options d'association des fichiers .py

Ajoutez PyCharm au PATH si proposé

Créez un nouveau projet dans un répertoire vide, pour permettre la création automatique d’un environnement virtuel (venv).

Activez l’import automatique dans PyCharm :
Settings → Editor → General → Auto Import

Guide pour lancer le projet
1. Importer la base de données
Lancez le serveur MySQL.

Importez le fichier DUMP SQL fourni, qui crée la base Mathias_Murillo_module164 avec ses tables et données.

Vous pouvez aussi exécuter ce script depuis PyCharm :
database/1_ImportationDumpSql.py (clic droit → Run)

2. Tester la connexion à la base de données
Lancez le script :
database/2_test_connection_bd.py
pour vérifier que tout fonctionne.

3. Démarrer le serveur Flask
Exécutez le fichier :
run_mon_app.py (clic droit → Run)

Puis, dans la console, ouvrez le lien suivant dans votre navigateur :
http://127.0.0.1:5005/

Navigation dans l’interface web
Imprimante : affichage, ajout, modification et suppression

Personne : affichage, ajout et suppression

Filament : affichage uniquement (lecture seule)

Fichiers Utilisables : affichage des fichiers d’impression

Réservation : création et visualisation des réservations d’imprimantes

Auteur : Mathias Murillo – EXPI1A
