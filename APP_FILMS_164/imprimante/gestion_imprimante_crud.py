"""Gestion des "routes" FLASK et des données pour les imprimante.
Fichier : gestion_imprimante_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.imprimante.gestion_imprimante_wtf_forms import FormWTFAjouterImprimante
from APP_FILMS_164.imprimante.gestion_imprimante_wtf_forms import FormWTFDeleteImprimante
from APP_FILMS_164.imprimante.gestion_imprimante_wtf_forms import FormWTFUpdateImprimante

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /imprimante_afficher

    Test : ex : http://127.0.0.1:5575/imprimante_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les imprimante.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/imprimante_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def imprimante_afficher(order_by, id_genre_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_imprimante_afficher = """SELECT *  FROM imprimante ORDER BY id_imprimante ASC"""
                    mc_afficher.execute(strsql_imprimante_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_imprimante"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du imprimante sélectionné avec un nom de variable
                    valeur_id_imprimante_selected_dictionnaire = {"value_id_imprimante_selected": id_genre_sel}
                    strsql_imprimante_afficher = """SELECT *  FROM imprimante WHERE id_imprimante = %(value_id_imprimante_selected)s"""

                    mc_afficher.execute(strsql_imprimante_afficher, valeur_id_imprimante_selected_dictionnaire)
                else:
                    strsql_imprimante_afficher = """SELECT *  FROM imprimante ORDER BY id_imprimante DESC"""

                    mc_afficher.execute(strsql_imprimante_afficher)

                data_imprimante = mc_afficher.fetchall()

                print("data_imprimante ", data_imprimante, " Type : ", type(data_imprimante))

                # Différencier les messages si la table est vide.
                if not data_imprimante and id_genre_sel == 0:
                    flash("""La table "t_imprimante
" est vide. !!""", "warning")
                elif not data_imprimante and id_genre_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le imprimante demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données imprimante affichés !!", "success")

        except Exception as exception_imprimante_afficher:
            raise ExceptionImprimanteAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{imprimante_afficher.__name__} ; "
                                          f"{exception_imprimante_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("imprimante/imprimante_afficher.html", data=data_imprimante)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5575/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "name_genre_html" du formulaire "imprimante/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/imprimante_ajouter", methods=['GET', 'POST'])
def imprimante_ajouter_wtf():
    form = FormWTFAjouterImprimante()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                name_genre_wtf = form.nom_genre_wtf.data
                name_genre = name_genre_wtf.lower()
                name_marque_wtf = form.marque_wtf.data;
                valeurs_insertion_dictionnaire = {"value_intitule_genre": name_genre,
                                                  "value_marque": name_marque_wtf,
                                                  }
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO imprimante (id_imprimante,entretien,marque) VALUES (NULL,%(value_intitule_genre)s,%(value_marque)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('imprimante_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as Exception_imprimante_ajouter_wtf:
            raise ExceptionimprimanteAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{imprimante_ajouter_wtf.__name__} ; "
                                            f"{Exception_imprimante_ajouter_wtf}")

    return render_template("imprimante/imprimante_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update

    Test : ex cliquer sur le menu "imprimante" puis cliquer sur le bouton "EDIT" d'un "genre"

    Paramètres : sans

    But : Editer(update) un genre qui a été sélectionné dans le formulaire "imprimante_afficher.html"

    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "imprimante/imprimante_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/imprimante_update", methods=['GET', 'POST'])
def imprimante_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_imprimante"
    id_imprimante_update = request.values['id_imprimante_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateImprimante()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "imprimante_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_imprimante_update = form_update.nom_imprimante_update_wtf.data
            name_imprimante_update = name_imprimante_update.lower()
            date_imprimante_essai = form_update.date_imprimante_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_imprimante": id_imprimante_update,
                                          "value_name_imprimante": name_imprimante_update,
                                          "value_date_imprimante_essai": date_imprimante_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intituleimprimante = """UPDATE t_imprimante SET intitule_imprimante = %(value_name_imprimante)s, 
            date_ins_imprimante = %(value_date_imprimante_essai)s WHERE id_imprimante = %(value_id_imprimante)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intituleimprimante, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_imprimante_update"
            return redirect(url_for('imprimante_afficher', order_by="ASC", id_imprimante_sel=id_imprimante_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_imprimante" et "intitule_imprimante" de la "t_imprimante"
            str_sql_id_imprimante = "SELECT id_imprimante, intitule_imprimante, date_ins_imprimante FROM t_imprimante " \
                               "WHERE id_imprimante = %(value_id_imprimante)s"
            valeur_select_dictionnaire = {"value_id_imprimante": id_imprimante_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_imprimante, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom imprimante" pour l'UPDATE
            data_nom_imprimante = mybd_conn.fetchone()
            print("data_nom_imprimante ", data_nom_imprimante, " type ", type(data_nom_imprimante), " imprimante ",
                  data_nom_imprimante["intitule_imprimante"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "imprimante_update_wtf.html"
            form_update.nom_imprimante_update_wtf.data = data_nom_imprimante["intitule_imprimante"]
            form_update.date_imprimante_wtf_essai.data = data_nom_imprimante["date_ins_imprimante"]

    except Exception as Exception_imprimante_update_wtf:
        raise ExceptionimprimanteUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{imprimante_update_wtf.__name__} ; "
                                      f"{Exception_imprimante_update_wtf}")

    return render_template("imprimante/imprimante_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /imprimante_delete

    Test : ex. cliquer sur le menu "imprimante" puis cliquer sur le bouton "DELETE" d'un "imprimante"

    Paramètres : sans

    But : Effacer(delete) un imprimante qui a été sélectionné dans le formulaire "imprimante_afficher.html"

    Remarque :  Dans le champ "nom_imprimante_delete_wtf" du formulaire "imprimante/imprimante_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/imprimante_delete", methods=['GET', 'POST'])
def imprimante_delete_wtf():
    data_films_attribue_imprimante_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_imprimante"
    id_imprimante_delete = request.values['id_imprimante_btn_delete_html']

    # Objet formulaire pour effacer le imprimante sélectionné.
    form_delete = FormWTFDeleteImprimante()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("imprimante_afficher", order_by="ASC", id_imprimante_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "imprimante/imprimante_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_imprimante_delete = session['data_films_attribue_imprimante_delete']
                print("data_films_attribue_imprimante_delete ", data_films_attribue_imprimante_delete)

                flash(f"Effacer le imprimante de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer imprimante" qui va irrémédiablement EFFACER le imprimante
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_imprimante": id_imprimante_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_imprimante = """DELETE FROM t_imprimante_film WHERE fk_imprimante = %(value_id_imprimante)s"""
                str_sql_delete_idimprimante = """DELETE FROM t_imprimante WHERE id_imprimante = %(value_id_imprimante)s"""
                # Manière brutale d'effacer d'abord la "fk_imprimante", même si elle n'existe pas dans la "t_imprimante_film"
                # Ensuite on peut effacer le imprimante vu qu'il n'est plus "lié" (INNODB) dans la "t_imprimante_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_imprimante, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idimprimante, valeur_delete_dictionnaire)

                flash(f"imprimante définitivement effacé !!", "success")
                print(f"imprimante définitivement effacé !!")

                # afficher les données
                return redirect(url_for('imprimante_afficher', order_by="ASC", id_imprimante_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_imprimante": id_imprimante_delete}
            print(id_imprimante_delete, type(id_imprimante_delete))

            # Requête qui affiche tous les films_imprimante qui ont le imprimante que l'utilisateur veut effacer
            str_sql_imprimante_films_delete = """SELECT id_imprimante_film, nom_film, id_imprimante, intitule_imprimante FROM t_imprimante_film 
                                            INNER JOIN t_film ON t_imprimante_film.fk_film = t_film.id_film
                                            INNER JOIN t_imprimante ON t_imprimante_film.fk_imprimante = t_imprimante.id_imprimante
                                            WHERE fk_imprimante = %(value_id_imprimante)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_imprimante_films_delete, valeur_select_dictionnaire)
                data_films_attribue_imprimante_delete = mydb_conn.fetchall()
                print("data_films_attribue_imprimante_delete...", data_films_attribue_imprimante_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "imprimante/imprimante_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_imprimante_delete'] = data_films_attribue_imprimante_delete

                # Opération sur la BD pour récupérer "id_imprimante" et "intitule_imprimante" de la "t_imprimante"
                str_sql_id_imprimante = "SELECT id_imprimante, intitule_imprimante FROM t_imprimante WHERE id_imprimante = %(value_id_imprimante)s"

                mydb_conn.execute(str_sql_id_imprimante, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom imprimante" pour l'action DELETE
                data_nom_imprimante = mydb_conn.fetchone()
                print("data_nom_imprimante ", data_nom_imprimante, " type ", type(data_nom_imprimante), " imprimante ",
                      data_nom_imprimante["intitule_imprimante"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "imprimante_delete_wtf.html"
            form_delete.nom_imprimante_delete_wtf.data = data_nom_imprimante["intitule_imprimante"]

            # Le bouton pour l'action "DELETE" dans le form. "imprimante_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_imprimante_delete_wtf:
        raise ExceptionimprimanteDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{imprimante_delete_wtf.__name__} ; "
                                      f"{Exception_imprimante_delete_wtf}")

    return render_template("imprimante/imprimante_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_imprimante_delete)