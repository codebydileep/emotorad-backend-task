from flask import Flask, request, jsonify, abort
from models import db, Contact
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Initialize database tables when the app starts
with app.app_context():
    db.create_all()

@app.route('/identify', methods=['POST'])
def identify():
    data = request.json
    
    # Error handling for missing email and phone number
    if not data or not ("email" in data or "phoneNumber" in data):
        abort(400, description="Request must include an email or phoneNumber")
    
    email = data.get("email")
    phoneNumber = data.get("phoneNumber")
    
    # Query existing contacts with matching email or phoneNumber
    existing_contacts = Contact.query.filter(
        (Contact.email == email) | (Contact.phoneNumber == phoneNumber)
    ).all()

    if not existing_contacts:
        # No existing contact, create a new primary contact
        new_contact = Contact(
            email=email,
            phoneNumber=phoneNumber,
            linkPrecedence="primary",
            createdAt=datetime.utcnow()
        )
        db.session.add(new_contact)
        db.session.commit()
        primary_contact = new_contact
    else:
        # Existing contacts found, determine primary contact
        primary_contact = min(existing_contacts, key=lambda c: c.createdAt)
        
        # Check if there is new information to add as secondary contact
        new_info = (email and email != primary_contact.email) or \
                   (phoneNumber and phoneNumber != primary_contact.phoneNumber)

        if new_info:
            # Add new information as a secondary contact
            secondary_contact = Contact(
                email=email,
                phoneNumber=phoneNumber,
                linkedId=primary_contact.id,
                linkPrecedence="secondary",
                createdAt=datetime.utcnow()
            )
            db.session.add(secondary_contact)
            db.session.commit()

    # Gather all linked contacts for the response
    contacts = Contact.query.filter(
        (Contact.id == primary_contact.id) | (Contact.linkedId == primary_contact.id)
    ).all()

    # Extract emails, phone numbers, and secondary contact IDs
    emails = list(set(c.email for c in contacts if c.email))
    phoneNumbers = list(set(c.phoneNumber for c in contacts if c.phoneNumber))
    secondary_ids = [c.id for c in contacts if c.linkPrecedence == "secondary"]

    response = {
        "primaryContactId": primary_contact.id,
        "emails": emails,
        "phoneNumbers": phoneNumbers,
        "secondaryContactIds": secondary_ids
    }

    return jsonify(response), 200

# Error handling for JSON decoding and invalid requests
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400
9999999
if __name__ == '__main__':
    app.run(debug=True, port=5001)
