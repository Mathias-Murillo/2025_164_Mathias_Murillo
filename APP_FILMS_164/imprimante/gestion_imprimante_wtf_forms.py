"""
    Fichier : gestion_imprimante_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterImprimante(FlaskForm):
    """
        Dans le formulaire "imprimante_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_genre_wtf = StringField("modéle ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(nom_genre_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    marque_regexp = ""  # OM 2025.03.20 à vous de trouver la regexp qui vous convient pour votre application de la marque
    marque_wtf = StringField("Clavioter la marque ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(marque_regexp,
                                                                          message="Il faudra changer la regexp pour "
                                                                                  "votre application")
                                                                   ])

    submit = SubmitField("Enregistrer l'imprimante")


class FormWTFUpdateImprimante(FlaskForm):
    """
        Dans le formulaire "imprimante_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\-]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"

    nom_genre_update_wtf = StringField("modéle ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    date_genre_wtf_essai = DateField("Essai date", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update genre")


class FormWTFDeleteImprimante(FlaskForm):
    """
        Dans le formulaire "imprimante_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    nom_genre_delete_wtf = StringField("Effacer ce genre")
    submit_btn_del = SubmitField("Effacer genre")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")


