from monapp import app
from flask import render_template, redirect, url_for, flash, request
from monapp import monapp, db
from monapp.models import User, Event, Reservation
from flask_login import login_user, logout_user, current_user, login_required

# Définition d'une route Flask
@app.route('/')
# Fonction home
def home():
    events = Event.query.all()
    return render_template('events.html', events=events)

# Définition d'une route Flask
@app.route('/dashboard')
@login_required
# Fonction dashboard
def dashboard():
    events = Event.query.all()
    return render_template('dashboard.html', events=events)

# Définition d'une route Flask
@app.route('/register', methods=['GET', 'POST'])
# Fonction register
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Compte créé avec succès !')
        return redirect(url_for('login'))
    return render_template('register.html')

# Définition d'une route Flask
@app.route('/login', methods=['GET', 'POST'])
# Fonction login
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            flash('Connexion réussie')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou mot de passe incorrect')
    return render_template('login.html')

# Définition d'une route Flask
@app.route('/logout')
@login_required
# Fonction logout
def logout():
    logout_user()
    flash('Déconnecté avec succès')
    return redirect(url_for('home'))

# Définition d'une route Flask
@app.route('/reserver/<int:event_id>')
@login_required
# Fonction reserver
def reserver(event_id):
    reservation = Reservation(user_id=current_user.id, event_id=event_id, status='confirmé')
    db.session.add(reservation)
    db.session.commit()
    flash('Réservation confirmée !')
    return redirect(url_for('dashboard'))

# Définition d'une route Flask
@app.route('/annuler/<int:reservation_id>')
@login_required
# Fonction annuler_reservation
def annuler_reservation(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    if reservation.user_id != current_user.id:
        flash('Vous ne pouvez pas annuler cette réservation.')
        return redirect(url_for('dashboard'))
    reservation.status = 'annulé'
    db.session.commit()
    flash('Réservation annulée.')
    return redirect(url_for('dashboard'))


# Définition d'une route Flask
@app.route('/admin/ajouter', methods=['GET', 'POST'])
@login_required
# Fonction ajouter_evenement
def ajouter_evenement():
    if request.method == 'POST':
        titre = request.form['title']
        description = request.form['description']
        date = request.form['date']
        categorie = request.form['category']
        event = Event(title=titre, description=description, date=date, category=categorie)
        db.session.add(event)
        db.session.commit()
        flash('Événement ajouté !')
        return redirect(url_for('dashboard'))
    return render_template('ajouter_event.html')

# Définition d'une route Flask
@app.route('/admin/modifier/<int:event_id>', methods=['GET', 'POST'])
@login_required
# Fonction modifier_evenement
def modifier_evenement(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.description = request.form['description']
        event.date = request.form['date']
        event.category = request.form['category']
        db.session.commit()
        flash('Événement mis à jour !')
        return redirect(url_for('dashboard'))
    return render_template('modifier_event.html', event=event)

# Définition d'une route Flask
@app.route('/admin/supprimer/<int:event_id>')
@login_required
# Fonction supprimer_evenement
def supprimer_evenement(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash('Événement supprimé.')
    return redirect(url_for('dashboard'))
