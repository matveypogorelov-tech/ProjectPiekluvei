from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                                    'aptieka.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super_slepens_atslegas_vards'
db = SQLAlchemy(app)


class Kategorija(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nosaukums = db.Column(db.String(50), nullable=False)


class Medikaments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nosaukums = db.Column(db.String(100), nullable=False)
    cena = db.Column(db.Float, nullable=False)
    apraksts = db.Column(db.Text, nullable=True)
    kategorija_id = db.Column(db.Integer, db.ForeignKey('kategorija.id'), nullable=False)


class Lietotajs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lietotajvards = db.Column(db.String(50), unique=True, nullable=False)
    parole_hash = db.Column(db.String(200), nullable=False)
    loma = db.Column(db.String(20), default='lietotajs')


@app.context_processor
def inject_categories():
    try:
        visas_kategorijas = Kategorija.query.all()
        return dict(global_kategorijas=visas_kategorijas)
    except:
        return dict(global_kategorijas=[])


def inicializet_datus():
    if Kategorija.query.first() is None:
        kat_nosaukumi = ["Vitamīni un Minerālvielas", "Kosmētika", "Matu kopšanai", "Medikamenti", "Higiēna",
                         "Māmiņa un Bērns"]
        kategorijas = []
        for nos in kat_nosaukumi:
            kat = Kategorija(nosaukums=nos)
            db.session.add(kat)
            kategorijas.append(kat)
        db.session.commit()

        # 1. Vitamīni un Minerālvielas (kategorijas[0])
        preces = [
            Medikaments(nosaukums="D3 Vitamīns 4000 IU", cena=9.50, apraksts="Imunitātei un kaulu veselībai",
                        kategorija_id=kategorijas[0].id),
            Medikaments(nosaukums="C Vitamīns 1000mg", cena=6.20, apraksts="Spēcīgs antioksidants",
                        kategorija_id=kategorijas[0].id),
            Medikaments(nosaukums="Möller's Zivju Eļļa", cena=14.99, apraksts="Sirds un asinsvadu veselībai, Omega-3",
                        kategorija_id=kategorijas[0].id),
            Medikaments(nosaukums="Magnijs + B6", cena=8.30, apraksts="Nervu sistēmas un muskuļu darbībai",
                        kategorija_id=kategorijas[0].id),
            Medikaments(nosaukums="Komplekss matiem un nagiem", cena=18.50,
                        apraksts="Skaistumam un veselībai no iekšienes", kategorija_id=kategorijas[0].id),

            # 2. Kosmētika (kategorijas[1])
            Medikaments(nosaukums="Bioderma Micelārais Ūdens 500ml", cena=16.90, apraksts="Jutīgas ādas attīrīšanai",
                        kategorija_id=kategorijas[1].id),
            Medikaments(nosaukums="Eucerin Mitrinošs Sejas Krēms", cena=22.50, apraksts="Intensīva mitrināšana 24h",
                        kategorija_id=kategorijas[1].id),
            Medikaments(nosaukums="Vichy Pretnovecošanās Serums", cena=35.00,
                        apraksts="Grumbu samazināšanai un sejas ovālam", kategorija_id=kategorijas[1].id),
            Medikaments(nosaukums="La Roche-Posay SPF 50+ Krēms", cena=19.80,
                        apraksts="Augsta aizsardzība pret sauli sejas ādai", kategorija_id=kategorijas[1].id),
            Medikaments(nosaukums="Nomierinoša Sejas Maska ar Māliem", cena=4.50,
                        apraksts="Poru attīrīšanai un ādas tonizēšanai", kategorija_id=kategorijas[1].id),

            # 3. Matu kopšanai (kategorijas[2])
            Medikaments(nosaukums="Vichy Dercos Pretblaugznu Šampūns", cena=15.99,
                        apraksts="Efektīvi novērš blaugznas jau pēc 1. reizes", kategorija_id=kategorijas[2].id),
            Medikaments(nosaukums="Matu augšanu veicinošs serums", cena=25.50,
                        apraksts="Stimulē asinsriti un matu folikulus", kategorija_id=kategorijas[2].id),
            Medikaments(nosaukums="Barojoša Maska ar Argāna Eļļu", cena=11.20, apraksts="Sausiem un bojātiem matiem",
                        kategorija_id=kategorijas[2].id),
            Medikaments(nosaukums="Sausais Šampūns Batiste", cena=5.90,
                        apraksts="Ātrai matu atsvaidzināšanai starp mazgāšanas reizēm",
                        kategorija_id=kategorijas[2].id),
            Medikaments(nosaukums="Kondicionieris Krāsotiem Matiem", cena=8.50,
                        apraksts="Aizsargā krāsu no izbalēšanas", kategorija_id=kategorijas[2].id),

            # 4. Medikamenti (kategorijas[3])
            Medikaments(nosaukums="Ibumetin 400mg N10", cena=3.50, apraksts="Pretsāpju un iekaisuma mazinošs līdzeklis",
                        kategorija_id=kategorijas[3].id),
            Medikaments(nosaukums="Paracetamol 500mg N20", cena=2.80, apraksts="Temperatūras un sāpju mazināšanai",
                        kategorija_id=kategorijas[3].id),
            Medikaments(nosaukums="Xymelin Pretiesnu Aerosols", cena=6.20, apraksts="Ātri atbrīvo aizliktu degunu",
                        kategorija_id=kategorijas[3].id),
            Medikaments(nosaukums="Brontex Klepus Sīrups", cena=5.40, apraksts="Atkrēpošanas veicināšanai",
                        kategorija_id=kategorijas[3].id),
            Medikaments(nosaukums="Voltaren Ziede 50g", cena=9.90,
                        apraksts="Lokālai muskuļu un locītavu sāpju mazināšanai", kategorija_id=kategorijas[3].id),
            Medikaments(nosaukums="Mezym Forte N20", cena=4.50, apraksts="Uzlabo gremošanu",
                        kategorija_id=kategorijas[3].id),

            # 5. Higiēna (kategorijas[4])
            Medikaments(nosaukums="Sensodyne Zobu Pasta 75ml", cena=4.90, apraksts="Jutīgu zobu ikdienas kopšanai",
                        kategorija_id=kategorijas[4].id),
            Medikaments(nosaukums="Listerine Mutes Skalojamais Līdz. 500ml", cena=6.50,
                        apraksts="Aizsardzība pret aplikumu un svaiga elpa", kategorija_id=kategorijas[4].id),
            Medikaments(nosaukums="Dušas Želeja Jutīgai Ādai 400ml", cena=8.20, apraksts="Bez ziepēm un parabēniem",
                        kategorija_id=kategorijas[4].id),
            Medikaments(nosaukums="Vates Plāksnītes N100", cena=1.20, apraksts="100% kokvilna kosmētikas noņemšanai",
                        kategorija_id=kategorijas[4].id),
            Medikaments(nosaukums="Dezodorants Rullītis 50ml", cena=3.80, apraksts="Aizsardzība pret svīšanu 48h",
                        kategorija_id=kategorijas[4].id),

            # 6. Māmiņa un Bērns (kategorijas[5])
            Medikaments(nosaukums="Bepanthen Ziede 30g", cena=7.50,
                        apraksts="Bērna ādas iekaisumu un nobrāzumu kopšanai", kategorija_id=kategorijas[5].id),
            Medikaments(nosaukums="Pampers Mitrās Salvetes N52", cena=2.99, apraksts="Maigas salvetes ar kumelītēm",
                        kategorija_id=kategorijas[5].id),
            Medikaments(nosaukums="Bērnu Zobu Birste (0-2 gadi)", cena=3.10, apraksts="Ar mīkstiem sariņiem",
                        kategorija_id=kategorijas[5].id),
            Medikaments(nosaukums="NUK Māneklītis Silikona", cena=4.50, apraksts="Ortodontiskās formas knupītis",
                        kategorija_id=kategorijas[5].id),
            Medikaments(nosaukums="Zīdaiņu Vanniņas Eļļa 200ml", cena=12.90,
                        apraksts="Maigai ādas attīrīšanai un mitrināšanai", kategorija_id=kategorijas[5].id)
        ]

        db.session.add_all(preces)
        db.session.commit()

    if Lietotajs.query.filter_by(lietotajvards='admin').first() is None:
        admin = Lietotajs(lietotajvards='admin', parole_hash=generate_password_hash('admin123'), loma='admin')
        db.session.add(admin)
        db.session.commit()


@app.route('/', methods=['GET'])
def sakumlapa():
    vaicajums = request.args.get('meklet', '').lower()
    kategorija_filtrs = request.args.get('kategorija')
    ipass_filtrs = request.args.get('ipass')

    query = Medikaments.query

    if kategorija_filtrs:
        query = query.filter_by(kategorija_id=kategorija_filtrs)

    visi_medikamenti = query.all()

    if ipass_filtrs == 'akcijas':
        akcijas_atslegvardi = ["d3", "bioderma", "ibumetin", "sensodyne", "pampers", "dercos"]
        visi_medikamenti = [med for med in visi_medikamenti if
                            any(v in med.nosaukums.lower() for v in akcijas_atslegvardi)]

    elif ipass_filtrs == 'zvaigznes':
        visi_medikamenti = [med for med in visi_medikamenti if med.kategorija_id == 2 and med.cena >= 10.00]

    elif ipass_filtrs == 'spf':
        visi_medikamenti = [med for med in visi_medikamenti if
                            'spf' in med.nosaukums.lower() or (med.apraksts and 'spf' in med.apraksts.lower())]

    if vaicajums:
        visi_medikamenti = [med for med in visi_medikamenti if
                            vaicajums in med.nosaukums.lower() or (med.apraksts and vaicajums in med.apraksts.lower())]

    visi_medikamenti.sort(key=lambda x: x.cena)
    kategoriju_vardnica = {kat.id: kat.nosaukums for kat in Kategorija.query.all()}

    return render_template('index.html', medikamenti=visi_medikamenti, kategorijas=kategoriju_vardnica,
                           vaicajums=vaicajums)


@app.route('/pieslegties', methods=['GET', 'POST'])
def pieslegties():
    if request.method == 'POST':
        lietotajvards = request.form.get('lietotajvards')
        parole = request.form.get('parole')
        lietotajs = Lietotajs.query.filter_by(lietotajvards=lietotajvards).first()
        if lietotajs and check_password_hash(lietotajs.parole_hash, parole):
            session['lietotaja_id'] = lietotajs.id
            session['loma'] = lietotajs.loma
            session['lietotajvards'] = lietotajs.lietotajvards
            return redirect(url_for('sakumlapa'))
        else:
            flash('Nepareizs lietotājvārds vai parole!')
    return render_template('pieslegties.html')


@app.route('/registreties', methods=['GET', 'POST'])
def registreties():
    if request.method == 'POST':
        lietotajvards = request.form.get('lietotajvards')
        parole = request.form.get('parole')
        esošais_lietotajs = Lietotajs.query.filter_by(lietotajvards=lietotajvards).first()
        if esošais_lietotajs:
            flash('Šāds lietotājvārds jau eksistē!')
        else:
            jauns_lietotajs = Lietotajs(lietotajvards=lietotajvards, parole_hash=generate_password_hash(parole))
            db.session.add(jauns_lietotajs)
            db.session.commit()
            flash('Reģistrācija veiksmīga! Tagad varat pieslēgties.')
            return redirect(url_for('pieslegties'))
    return render_template('registreties.html')


@app.route('/iziet')
def iziet():
    session.clear()
    return redirect(url_for('sakumlapa'))


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('loma') != 'admin':
        return "Tev nav pieejas šai lapai!", 403

    if request.method == 'POST':
        nosaukums = request.form.get('nosaukums')
        cena = float(request.form.get('cena'))
        apraksts = request.form.get('apraksts')
        kategorija_id = int(request.form.get('kategorija_id'))
        jauns_medikaments = Medikaments(nosaukums=nosaukums, cena=cena, apraksts=apraksts, kategorija_id=kategorija_id)
        db.session.add(jauns_medikaments)
        db.session.commit()
        return redirect(url_for('admin'))

    visi_medikamenti = Medikaments.query.all()
    return render_template('admin.html', medikamenti=visi_medikamenti)


@app.route('/dzest/<int:id>')
def dzest_medikamentu(id):
    if session.get('loma') == 'admin':
        medikaments = Medikaments.query.get(id)
        if medikaments:
            db.session.delete(medikaments)
            db.session.commit()
    return redirect(url_for('admin'))

@app.route('/pievienot_grozam/<int:id>')
def pievienot_grozam(id):
    # Pārbaudām, vai lietotājs ir pieslēdzies
    if 'lietotaja_id' not in session:
        flash('Lai pievienotu preces grozam, lūdzu, pieslēdzieties savam profilam!')
        return redirect(url_for('pieslegties'))

    if 'grozs' not in session:
        session['grozs'] = {}

    grozs = session['grozs']
    preces_id_str = str(id)

    if preces_id_str in grozs:
        grozs[preces_id_str] += 1
    else:
        grozs[preces_id_str] = 1

    session.modified = True
    flash('Prece pievienota grozam!')
    return redirect(request.referrer or url_for('sakumlapa'))


@app.route('/grozs')
def grozs():
    if 'lietotaja_id' not in session:
        flash('Lūdzu, pieslēdzieties, lai apskatītu grozu!')
        return redirect(url_for('pieslegties'))

    grozs = session.get('grozs', {})
    preces_groza = []
    kopsumma = 0

    for preces_id, skaits in grozs.items():
        medikaments = Medikaments.query.get(int(preces_id))
        if medikaments:
            summa = medikaments.cena * skaits
            kopsumma += summa
            preces_groza.append({
                'medikaments': medikaments,
                'skaits': skaits,
                'summa': summa
            })

    return render_template('grozs.html', preces=preces_groza, kopsumma=kopsumma)


@app.route('/mainit_grozu/<int:id>/<darbiba>')
def mainit_grozu(id, darbiba):
    if 'grozs' in session:
        preces_id_str = str(id)
        if preces_id_str in session['grozs']:
            if darbiba == 'plus':
                session['grozs'][preces_id_str] += 1
            elif darbiba == 'minus':
                session['grozs'][preces_id_str] -= 1
                if session['grozs'][preces_id_str] <= 0:
                    del session['grozs'][preces_id_str]
            elif darbiba == 'dzest':
                del session['grozs'][preces_id_str]
            session.modified = True
    return redirect(url_for('grozs'))


@app.route('/iztuksot_grozu')
def iztuksot_grozu():
    session.pop('grozs', None)
    return redirect(url_for('grozs'))


@app.route('/samaksat')
def samaksat():
    if 'grozs' in session:
        session.pop('grozs', None)  # Iztukšojam grozu
        flash('Veiksmīgi samaksāts! Paldies par jūsu pirkumu!')
    return redirect(url_for('sakumlapa'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        inicializet_datus()
    app.run(debug=True)
