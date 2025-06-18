"""Gestion des "routes" FLASK et des données pour les filament.
Fichier : gestion_filament_crud.py b
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
from APP_FILMS_164.filament.gestion_filament_wtf_forms import FormWTFAjouterFilament
from APP_FILMS_164.filament.gestion_filament_wtf_forms import FormWTFDeleteFilament
from APP_FILMS_164.filament.gestion_filament_wtf_forms import FormWTFUpdateFilament

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /filament_afficher

    Test : ex : http://127.0.0.1:5575/filament_afficher

    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les filament.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/filament_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def filament_afficher(order_by, id_genre_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_filament_afficher = """SELECT *  FROM filament ORDER BY filament_id ASC"""
                    mc_afficher.execute(strsql_filament_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_filament"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du filament sélectionné avec un nom de variable
                    valeur_id_filament_selected_dictionnaire = {"value_id_filament_selected": id_genre_sel}
                    strsql_filament_afficher = """SELECT *  FROM filament WHERE 	filament_id = %(value_id_filament_selected)s"""

                    mc_afficher.execute(strsql_filament_afficher, valeur_id_filament_selected_dictionnaire)
                else:
                    strsql_filament_afficher = """SELECT *  FROM filament ORDER BY 	filament_id DESC"""

                    mc_afficher.execute(strsql_filament_afficher)

                data_filament = mc_afficher.fetchall()

                print("data_filament ", data_filament, " Type : ", type(data_filament))

                # Différencier les messages si la table est vide.
                if not data_filament and id_genre_sel == 0:
                    flash("""La table "filament
" est vide. !!""", "warning")
                elif not data_filament and id_genre_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le filament demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données filament affichés !!", "success")

        except Exception as exception_filament_afficher:
            raise ExceptionFilamentAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{filament_afficher.__name__} ; "
                                          f"{exception_filament_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("filaments/filament_afficher.html", data=data_filament)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5575/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "name_genre_html" du formulaire "filaments/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


class ExceptionfilamentAjouterWtf:
    pass


@app.route("/filament_ajouter", methods=['GET', 'POST'])
def filament_ajouter_wtf():
    form = FormWTFAjouterFilament()
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

                strsql_insert_genre = """INSERT INTO filament (filament_id,entretien,marque) VALUES (NULL,%(value_intitule_genre)s,%(value_marque)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('filament_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as Exception_filament_ajouter_wtf:
            raise ExceptionfilamentAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{filament_ajouter_wtf.__name__} ; "
                                            f"{Exception_filament_ajouter_wtf}")

    return render_template("filaments/filament_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update

    Test : ex cliquer sur le menu "filament" puis cliquer sur le bouton "EDIT" d'un "genre"

    Paramètres : sans

    But : Editer(update) un genre qui a été sélectionné dans le formulaire "filament_afficher.html"

    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "filaments/filament_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/filament_update", methods=['GET', 'POST'])
def filament_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "filament_id"
    id_filament_update = request.values['id_filament_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateFilament()
    try:
        # 2023.05.14 OM S'il y a des listes déroulantes dans le formulaire
        # La validation pose quelques problèmes
        if request.method == "POST" and form_update.submit.data:
            # Récupèrer la valeur du champ depuis "filament_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_filament_update = form_update.nom_filament_update_wtf.data
            name_entretien_update = form_update.entretien_filament_update_wtf.data
            name_marque_update = form_update.marque_filament_update_wtf.data
            name_num_serie_update = form_update.num_serie_filament_update_wtf.data
            date_filament_essai = form_update.date_filament_wtf_essai.data

            valeur_update_dictionnaire = {"value_id_filament": id_filament_update,
                                          "value_name_filament": name_filament_update,
                                          "value_name_entretien": name_entretien_update,
                                          "value_name_marque": name_marque_update,
                                          "value_name_num_serie": name_num_serie_update,
                                          "value_date_filament_essai": date_filament_essai
                                          }
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulefilament = """UPDATE filament SET marque = %(value_name_marque)s, 
            entretien = %(value_date_filament_essai)s WHERE filament_id = %(value_id_filament)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulefilament, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_filament_update"
            return redirect(url_for('filament_afficher', order_by="ASC", id_filament_sel=id_filament_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "filament_id" et "intitule_filament" de la "t_filament"
            str_sql_id_filament = "SELECT * FROM filament " \
                               "WHERE filament_id = %(value_id_filament)s"
            valeur_select_dictionnaire = {"value_id_filament": id_filament_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_filament, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom filament" pour l'UPDATE
            data_nom_filament = mybd_conn.fetchone()
            print("data_nom_filament ", data_nom_filament, " type ", type(data_nom_filament), " filament ",
                  data_nom_filament["num_serie"])

            # Afficher la valeur sélectionnée dans les champs du formulaire "filament_update_wtf.html"
            form_update.nom_filament_update_wtf.data = data_nom_filament["num_serie"]
            form_update.date_filament_wtf_essai.data = data_nom_filament["filament_id"]

    except Exception as Exception_filament_update_wtf:
        raise ExceptionfilamentUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{filament_update_wtf.__name__} ; "
                                      f"{Exception_filament_update_wtf}")

    return render_template("filaments/filament_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /filament_delete

    Test : ex. cliquer sur le menu "filament" puis cliquer sur le bouton "DELETE" d'un "filament"

    Paramètres : sans

    But : Effacer(delete) un filament qui a été sélectionné dans le formulaire "filament_afficher.html"

    Remarque :  Dans le champ "nom_filament_delete_wtf" du formulaire "filaments/filament_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/filament_delete", methods=['GET', 'POST'])
def filament_delete_wtf():
    data_films_attribue_filament_delete = None
    btn_submit_del = None
    id_filament_delete = request.values.get('id_filament_btn_delete_html')

    if not id_filament_delete:
        flash("ID d'filament manquant.", "danger")
        return redirect(url_for('filament_afficher', order_by="ASC", id_filament_sel=0))

    # Objet formulaire pour effacer l'filament sélectionnée
    form_delete = FormWTFDeleteFilament()

    try:
        if request.method == "POST" and form_delete.validate_on_submit():
            if form_delete.submit_btn_annuler.data:
                # L'utilisateur annule la suppression
                return redirect(url_for("filament_afficher", order_by="ASC", id_filament_sel=0, id_genre_sel=0))


            if form_delete.submit_btn_conf_del.data:
                # L'utilisateur est sur le point de confirmer la suppression
                data_films_attribue_filament_delete = session.get('data_films_attribue_filament_delete', None)
                if not data_films_attribue_filament_delete:
                    flash("Aucune donnée associée à cette filament.", "warning")
                    return redirect(url_for("filament_afficher", order_by="ASC", id_filament_sel=0, id_genre_sel=0))


                flash(f"Vous allez supprimer l'filament définitivement de la BD !!!", "danger")
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                # L'utilisateur confirme la suppression
                valeur_delete_dictionnaire = {"value_id_filament": id_filament_delete}

                str_sql_delete_films_filament = """DELETE FROM filaments_filament WHERE Filament_Fk = %(value_id_filament)s"""
                str_sql_delete_reservation = """DELETE FROM reservation WHERE filament_id = %(value_id_filament)s"""
                str_sql_delete_filament = """DELETE FROM filament WHERE filament_id = %(value_id_filament)s"""

                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_filament, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_reservation, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_filament, valeur_delete_dictionnaire)

                flash(f"Filament définitivement supprimée !", "success")
                return redirect(url_for('filament_afficher', order_by="ASC", id_filament_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_filament": id_filament_delete}
            str_sql_filament_films_delete = """SELECT * FROM filament
                                                 INNER JOIN fichier_utiliser ON filament.fichier = fichier_utiliser.id_fichier
                                                 WHERE filament.filament_id = %(value_id_filament)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_filament_films_delete, valeur_select_dictionnaire)
                data_films_attribue_filament_delete = mydb_conn.fetchall()
                session['data_films_attribue_filament_delete'] = data_films_attribue_filament_delete

                str_sql_id_filament = "SELECT filament_id, marque FROM filament WHERE filament_id = %(value_id_filament)s"
                mydb_conn.execute(str_sql_id_filament, valeur_select_dictionnaire)
                data_nom_filament = mydb_conn.fetchone()

            if data_nom_filament:
                form_delete.nom_filament_delete_wtf.data = data_nom_filament["marque"]
            else:
                flash("Filament introuvable.", "danger")
                return redirect(url_for('filament_afficher', order_by="ASC", id_filament_sel=0))

            btn_submit_del = False

    except Exception as e:
        flash(f"Une erreur est survenue : {str(e)}", "danger")
        return redirect(url_for('filament_afficher', order_by="ASC", id_filament_sel=0))

    return render_template("filaments/filament_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_filament_delete)
