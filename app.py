# coding : utf-8
# Vélo : Félix RIAT
# Réparation : Maxence FRECHIN
# Loue : Valentin MOUGENOT
# Ramène : Julien MOURCELY


from flask import Flask, request, render_template, redirect, url_for, abort, flash
import pymysql.cursors

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'

mydb = pymysql.connect(  # pymysql.connect remplace mysql.connector
    host="localhost",  # localhost sur les machines perso.
    user="friat",
    password="2801",
    database="BDD_friat",
    charset='utf8mb4',  # 2 attributs à ajouter
    cursorclass=pymysql.cursors.DictCursor  # 2 attributs à ajouter
)

mycursor = mydb.cursor()


@app.route('/')
def show_accueil():
    return render_template('layout.html')


@app.route('/reparation/show')
def show_reparation():
    mycursor.execute("SELECT * FROM REPARATION")
    reparation = mycursor.fetchall()
    return render_template('reparation/show_reparation.html', reparation=reparation)


@app.route('/reparation/delete')
def delete_reparation():
    id = request.args.get('id_reparation', '')
    tuple_rep = (id)
    sql = "DELETE FROM REPARATION WHERE id_reparation = %s"
    mycursor.execute(sql, tuple_rep)
    return redirect(url_for('show_reparation'))


@app.route('/reparation/add', methods=['GET'])
def add_reparation():
    mycursor.execute("SELECT id_velo FROM VELO")
    velo = mycursor.fetchall();
    return render_template('reparation/add_reparation.html', velo=velo)


@app.route('/reparation/add', methods=['POST'])
def valid_add_reparation():
    libelle = request.form.get('libelle_reparation', '')
    date = request.form.get('date_reparation', '')
    descriptif = request.form.get('descriptif', '')
    id_velo = request.form.get('id_velo', '')
    tuple_reparation = (libelle, date, descriptif, id_velo)
    sql = "INSERT INTO REPARATION (libelle_reparation, date_reparation, descriptif, id_velo) VALUES (%s, %s, %s, %s)"
    mycursor.execute(sql, tuple_reparation)
    return redirect(url_for('show_reparation'))


@app.route('/reparation/edit/<id>', methods=['GET'])
def edit_reparation(id):
    mycursor.execute("SELECT * FROM REPARATION WHERE id_reparation = " + id)
    reparation = mycursor.fetchall()
    return render_template('reparation/edit_reparation.html', reparation=reparation)


@app.route('/reparation/edit', methods=['POST'])
def valid_edit_reparation():
    id = request.form.get('id_reparation', '')
    libelle = request.form.get('libelle_reparation', '')
    date = request.form.get('date_reparation', '')
    descriptif = request.form.get('descriptif', '')
    tuple_reparation = (libelle, date, descriptif, id)
    sql = "UPDATE REPARATION SET libelle_reparation = %s, date_reparation = %s, descriptif = %s WHERE id_reparation = %s"
    mycursor.execute(sql, tuple_reparation)
    return redirect(url_for('show_reparation'))


@app.route('/velo/show')
def show_velo():
    sql = "SELECT VELO.id_velo, VELO.date_achat, VELO.prix_par_mois, VELO.code_marque, VELO.id_type_velo, MARQUE.libelle_marque, TYPE_VELO.libelle_type FROM VELO JOIN MARQUE ON VELO.code_marque = MARQUE.code_marque JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo;"
    mycursor.execute(sql)
    velo = mycursor.fetchall()

    sql2 = "SELECT TYPE_VELO.libelle_type, COUNT(VELO.id_type_velo) AS NB_velo_total FROM VELO JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo GROUP BY VELO.id_type_velo;"
    mycursor.execute(sql2)
    velo_type = mycursor.fetchall()
    return render_template('velo/show_velo.html', velo=velo, velo_type=velo_type)


@app.route('/velo/add', methods=['GET'])
def add_velo():
    sql = "SELECT * FROM MARQUE;"
    mycursor.execute(sql)
    marques = mycursor.fetchall()
    sql2 = "SELECT * FROM TYPE_VELO;"
    mycursor.execute(sql2)
    types_velo = mycursor.fetchall()
    return render_template('velo/add_velo.html', marques=marques, types_velo=types_velo)


@app.route('/velo/add', methods=['POST'])
def valid_add_velo():
    date_achat = request.form.get('date_achat', '')
    prix_par_mois = request.form.get('prix_par_mois', '')
    code_marque = request.form.get('code_marque', '')
    id_type_velo = request.form.get('type_velo', '')
    tuple_add = (date_achat, prix_par_mois, code_marque, id_type_velo)
    print(tuple_add)
    sql = "INSERT INTO VELO(date_achat, prix_par_mois, code_marque, id_type_velo) VALUE (%s, %s, %s, %s);"

    print(sql)
    mycursor.execute(sql, tuple_add)
    mydb.commit()
    print(mycursor.rowcount, " was add.")

    return redirect(url_for('show_velo'))


@app.route('/velo/edit/<id>', methods=['GET'])
def edit_velo(id):
    sql = "SELECT * FROM MARQUE;"
    mycursor.execute(sql)
    marques = mycursor.fetchall()

    sql2 = "SELECT * FROM TYPE_VELO;"
    mycursor.execute(sql2)
    type_velo = mycursor.fetchall()

    tuple_edit = (id)
    sql3 = "SELECT * FROM VELO WHERE id_velo = %s;"
    mycursor.execute(sql3, tuple_edit)
    velo = mycursor.fetchone()
    print(id)
    return render_template('velo/edit_velo.html', velo=velo, marques=marques, type_velo=type_velo)


@app.route('/velo/edit', methods=['POST'])
def valid_edit_velo():
    id = request.form.get('id_velo', '')
    date_achat = request.form.get('date_achat', '')
    prix_par_mois = request.form.get('prix_par_mois', '')
    code_marque = request.form.get('code_marque', '')
    id_type_velo = request.form.get('type_velo', '')
    tuple_edit = (date_achat, prix_par_mois, code_marque, id_type_velo, id)
    print(tuple_edit)
    sql = "UPDATE VELO SET date_achat=%s, prix_par_mois=%s, code_marque=%s, id_type_velo=%s WHERE id_velo=%s;"
    mycursor.execute(sql, tuple_edit)

    return redirect(url_for('show_velo'))


@app.route('/velo/delete')
def delete_velo():
    id = request.args.get('id', '')
    tuple_delete = (id)
    sql = "DELETE FROM REPARATION WHERE id_velo = %s;"
    sql4 = "DELETE FROM VELO WHERE id_velo = %s;"
    sql3 = "DELETE FROM loue WHERE id_velo = %s;"
    sql2 = "DELETE FROM ramene WHERE id_velo = %s;"
    mycursor.execute(sql, tuple_delete)
    mycursor.execute(sql2, tuple_delete)
    mycursor.execute(sql3, tuple_delete)
    mycursor.execute(sql4, tuple_delete)
    return redirect(url_for('show_velo'))


@app.route('/loue/show', methods=['GET'])
def show_loue():
    mycursor.execute("SELECT * FROM loue")
    loue = mycursor.fetchall()
    mycursor.execute(
        "SELECT loue.id_etudiant, loue.id_velo, loue.date_location, ramene.date_retour, DATEDIFF(ramene.date_retour, loue.date_location) AS duree_location FROM loue JOIN ramene ON loue.id_etudiant = ramene.id_etudiant AND loue.id_velo = ramene.id_velo")
    etat = mycursor.fetchall()
    return render_template('loue/show_loue.html', loue=loue, etat=etat)


@app.route('/loue/show', methods=['POST'])
def valid_filter_loue():
    date_location = request.form.get('date_location', '')
    date_retour = request.form.get('date_retour', '')
    if date_retour == '' and date_location == '':
        return redirect(url_for('show_loue'))
    tuple_loue = (date_location, date_retour)
    sql = "SELECT loue.id_etudiant, loue.id_velo, loue.date_location, ramene.date_retour, DATEDIFF(ramene.date_retour, loue.date_location) AS duree_location FROM loue JOIN ramene ON loue.id_etudiant = ramene.id_etudiant AND loue.id_velo = ramene.id_velo WHERE date_location >= %s and date_retour <= %s"
    mycursor.execute(sql, tuple_loue)
    etat = mycursor.fetchall()
    print(etat)
    mycursor.execute("SELECT * FROM loue")
    loue = mycursor.fetchall()
    return render_template('loue/show_loue.html', loue=loue, etat=etat)

@app.route('/loue/add', methods=['GET'])
def add_loue():
    mycursor.execute("SELECT id_etudiant FROM ETUDIANT ORDER BY id_etudiant")
    etudiant = mycursor.fetchall()
    mycursor.execute("SELECT id_velo FROM VELO ORDER BY id_velo")
    velo = mycursor.fetchall()
    return render_template('loue/add_loue.html', etudiant=etudiant, velo=velo)


@app.route('/loue/add', methods=['POST'])
def valid_add_loue():
    id_velo = request.form.get('id_velo', '')
    id_etudiant = request.form.get('id_etudiant', '')
    date_location = request.form.get('date', '')
    caution = request.form.get('caution', '')
    tuple_loue = (id_velo, id_etudiant, date_location, caution)
    print(id_velo)
    print(id_etudiant)
    print(date_location)
    print(caution)
    sql = "INSERT INTO loue (id_velo, id_etudiant, date_location, caution) VALUE (%s, %s, %s, %s)"
    mycursor.execute(sql, tuple_loue)
    return redirect(url_for('show_loue'))


@app.route('/loue/delete')
def delete_loue():
    id_velo = request.args.get('id_velo', '')
    id_etudiant = request.args.get('id_etudiant', '')
    date_location = request.args.get('date_location', '')
    tuple_loue = (id_velo, id_etudiant, date_location)
    sql = "DELETE FROM loue WHERE id_velo = %s AND id_etudiant = %s AND date_location = %s"
    mycursor.execute(sql, tuple_loue)
    return redirect(url_for('show_loue'))


@app.route('/loue/edit/<id_velo>/<id_etudiant>/<date_location>', methods=['GET'])
def edit_loue(id_velo, id_etudiant, date_location):
    print('id :', id_etudiant, id_velo, date_location)
    tuple = (id_velo, id_etudiant, date_location)
    sql = "SELECT * FROM loue WHERE id_velo = %s AND id_etudiant = %s AND date_location = %s"
    mycursor.execute(sql, tuple)
    loue = mycursor.fetchall()
    mycursor.execute("SELECT id_etudiant FROM ETUDIANT ORDER BY id_etudiant")
    etudiant = mycursor.fetchall()
    mycursor.execute("SELECT id_velo FROM VELO ORDER BY id_velo")
    velo = mycursor.fetchall()
    return render_template('loue/edit_loue.html', loue=loue[0], etudiant=etudiant, velo=velo)


@app.route('/loue/edit', methods=['POST'])
def valid_edit_loue():
    id_velo_base = request.form.get('id_velo_base', '')
    id_etudiant_base = request.form.get('id_etudiant_base', '')
    date_base = request.form.get('date_base', '')
    id_velo = request.form.get('id_velo', '')
    id_etudiant = request.form.get('id_etudiant', '')
    date = request.form.get('date', '')
    caution = request.form.get('caution', '')
    tuple_loue = (id_velo, id_etudiant, date, caution, id_velo_base, id_etudiant_base, date_base)
    print(tuple_loue)
    sql = "UPDATE loue SET id_velo = %s ,id_etudiant = %s ,date_location = %s ,caution = %s  WHERE id_velo = %s AND id_etudiant = %s AND date_location = %s"
    mycursor.execute(sql, tuple_loue)
    return redirect(url_for('show_loue'))


@app.route('/ramene/show', methods=['GET'])
def show_ramene():
    mycursor.execute("SELECT * FROM ramene")
    ramene = mycursor.fetchall()
    mycursor.execute("SELECT COUNT(DISTINCT ramene.id_velo) AS nb_velo FROM ramene JOIN loue ON ramene.id_velo = loue.id_velo AND ramene.id_etudiant = loue.id_etudiant WHERE loue.date_location > DATE(NOW()) OR ramene.date_retour < DATE(NOW())")
    etat = mycursor.fetchall()
    mycursor.execute("SELECT DATE(NOW())")
    date = mycursor.fetchall()
    return render_template('ramene/show_ramene.html', ramene=ramene, etat=etat[0], selected_date=date[0]['DATE(NOW())'])


@app.route('/ramene/show',  methods=['POST'])
def valid_filter_ramene():
    date = request.form.get('date', '')
    if date == '':
        return redirect(url_for('show_ramene'))
    mycursor.execute("SELECT * FROM ramene")
    ramene = mycursor.fetchall()
    tuple_ramene = (date, date)
    sql = "SELECT COUNT(DISTINCT ramene.id_velo) AS nb_velo FROM ramene JOIN loue ON ramene.id_velo = loue.id_velo AND ramene.id_etudiant = ramene.id_etudiant WHERE loue.date_location > %s OR ramene.date_retour < %s"
    mycursor.execute(sql, tuple_ramene)
    etat = mycursor.fetchall()
    print(etat)
    return render_template('ramene/show_ramene.html', ramene=ramene, etat=etat[0], selected_date=date)

@app.route('/ramene/edit/<id_velo>/<id_etudiant>/<date_retour>', methods=['GET'])
def edit_ramene(id_velo, id_etudiant, date_retour):
    print('id :', id_etudiant, id_velo, date_retour)
    tuple = (id_velo, id_etudiant, date_retour)
    sql = "SELECT * FROM ramene WHERE id_velo = %s AND id_etudiant = %s AND date_retour = %s"
    mycursor.execute(sql, tuple)
    ramene = mycursor.fetchall()
    mycursor.execute("SELECT id_etudiant FROM ETUDIANT ORDER BY id_etudiant")
    etudiant = mycursor.fetchall()
    mycursor.execute("SELECT id_velo FROM VELO ORDER BY id_velo")
    velo = mycursor.fetchall()
    print(ramene)
    return render_template('ramene/edit_ramene.html', ramene=ramene[0], etudiant=etudiant, velo=velo)


@app.route('/ramene/edit', methods=['POST'])
def valid_edit_ramene():
    id_velo = request.form.get('id_velo', '')
    id_etudiant = request.form.get('id_etudiant', '')
    date = request.form.get('date', '')
    paiement = request.form.get('paiement', '')
    tuple_ramene = (id_velo, id_etudiant, date, paiement, id_velo, id_etudiant, date)
    print(tuple_ramene)
    sql = "UPDATE ramene SET id_velo = %s ,id_etudiant = %s ,date_location = %s ,paiement = %s  WHERE id_velo = %s AND id_etudiant = %s AND date_location = %s"
    mycursor.execute(sql, tuple_ramene)
    return redirect(url_for('show_ramene'))


@app.route('/ramene/delete')
def delete_ramene():
    id_velo = request.args.get('id_velo', '')
    id_etudiant = request.args.get('id_etudiant', '')
    date_retour = request.args.get('date_retour', '')
    tuple_ramene = (id_velo, id_etudiant, date_retour)
    sql = "DELETE FROM ramene WHERE id_velo = %s AND id_etudiant = %s AND date_retour = %s"
    mycursor.execute(sql, tuple_ramene)
    return redirect(url_for('show_ramene'))


@app.route('/ramene/add', methods=['GET'])
def add_ramene():
    mycursor.execute("SELECT id_etudiant FROM ETUDIANT ORDER BY id_etudiant")
    etudiant = mycursor.fetchall()
    mycursor.execute("SELECT id_velo FROM VELO ORDER BY id_velo")
    velo = mycursor.fetchall()
    return render_template('ramene/add_ramene.html', etudiant=etudiant, velo=velo)


@app.route('/ramene/add', methods=['POST'])
def valid_add_ramene():
    id_velo = request.form.get('id_velo', '')
    id_etudiant = request.form.get('id_etudiant', '')
    date_retour = request.form.get('date', '')
    paiement = request.form.get('paiement', '')
    tuple_ramene = (id_velo, id_etudiant, date_retour, paiement)
    sql = "INSERT INTO ramene (id_velo, id_etudiant, date_retour, paiement) VALUE (%s, %s, %s, %s)"
    mycursor.execute(sql, tuple_ramene)
    return redirect(url_for('show_ramene'))


if __name__ == '__main__':
    app.run()
