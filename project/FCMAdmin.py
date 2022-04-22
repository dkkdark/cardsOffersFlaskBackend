import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("/Users/blohinaksenia/PycharmProjects/backendForCardsApp/serviceAccountKey.json")
firebase_admin.initialize_app(cred)


def send_push(sender_id, title, msg, registration_token, card_id, card_title, card_cost):
    message = messaging.MulticastMessage(
        data={
            "id": sender_id,
            "title": title,
            "body": msg,
            "card_id": card_id,
            "card_title": card_title,
            "card_cost": card_cost,
        },
        tokens=registration_token,
    )

    response = messaging.send_multicast(message)
    print('Successfully sent message:', response)