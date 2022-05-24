CREATE TABLE TYPE_VELO(
   id_type_velo INT,
   libelle_type VARCHAR(20),
   PRIMARY KEY(id_type_velo)
);

CREATE TABLE ETUDIANT(
   id_etudiant INT,
   prenom VARCHAR(20),
   nom VARCHAR(20),
   adresse VARCHAR(50),
   tel VARCHAR(13),
   mail VARCHAR(50),
   PRIMARY KEY(id_etudiant)
);

CREATE TABLE PIECE(
   code_piece INT,
   libelle_piece VARCHAR(20),
   PRIMARY KEY(code_piece)
);

CREATE TABLE MARQUE(
   code_marque INT,
   libelle_marque VARCHAR(20),
   PRIMARY KEY(code_marque)
);

CREATE TABLE VELO(
   id_velo INT,
   date_achat DATE,
   prix_par_mois DOUBLE,
   code_marque INT NOT NULL,
   id_type_velo INT NOT NULL,
   PRIMARY KEY(id_velo),
   FOREIGN KEY(code_marque) REFERENCES MARQUE(code_marque),
   FOREIGN KEY(id_type_velo) REFERENCES TYPE_VELO(id_type_velo)
);

CREATE TABLE REPARATION(
   id_reparation INT,
   libelle_reparation VARCHAR(20),
   date_reparation DATE,
   descriptif TEXT,
   id_velo INT NOT NULL,
   PRIMARY KEY(id_reparation),
   FOREIGN KEY(id_velo) REFERENCES VELO(id_velo)
);

CREATE TABLE necessite(
   id_reparation INT,
   code_piece INT,
   quantite INT,
   PRIMARY KEY(id_reparation, code_piece),
   FOREIGN KEY(id_reparation) REFERENCES REPARATION(id_reparation),
   FOREIGN KEY(code_piece) REFERENCES PIECE(code_piece)
);

CREATE TABLE contribue(
   id_etudiant INT,
   id_reparation INT,
   PRIMARY KEY(id_etudiant, id_reparation),
   FOREIGN KEY(id_etudiant) REFERENCES ETUDIANT(id_etudiant),
   FOREIGN KEY(id_reparation) REFERENCES REPARATION(id_reparation)
);

CREATE TABLE loue(
   id_velo INT,
   id_etudiant INT,
   date_location DATE,
   caution DECIMAL(5,2),
   PRIMARY KEY(id_velo, id_etudiant),
   FOREIGN KEY(id_velo) REFERENCES VELO(id_velo),
   FOREIGN KEY(id_etudiant) REFERENCES ETUDIANT(id_etudiant)
);

CREATE TABLE ramene(
   id_velo INT,
   id_etudiant INT,
   date_retour DATE,
   paiement DOUBLE,
   PRIMARY KEY(id_velo, id_etudiant),
   FOREIGN KEY(id_velo) REFERENCES VELO(id_velo),
   FOREIGN KEY(id_etudiant) REFERENCES ETUDIANT(id_etudiant)
);


SELECT TYPE_VELO.libelle, COUNT(VELO.*) AS NB_velo_total FROM VELO JOIN TYPE_VELO ON VELO.id_type_velo = TYPE_VELO.id_type_velo GROUP BY VELO.id_type_velo;