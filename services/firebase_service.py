import time
from firebase_admin import firestore
from typing import List, Dict, Any

db = firestore.client()


class FirebaseService:
    @staticmethod
    def get_user_by_email(email: str):
        users_ref = db.collection("users")
        user_query = (
            users_ref.where(filter=firestore.FieldFilter("email", "==", email))
            .limit(1)
            .get()
        )
        return user_query[0] if user_query else None

    @staticmethod
    def store_sos(sos_data: Dict[str, Any], user_id: str):
        sos_data["user_ref"] = db.collection("users").document(user_id)
        return db.collection("sos_messages").add(sos_data)

    @staticmethod
    def update_sos_status(sos_id: str, status: str):
        return db.collection("sos_messages").document(sos_id).update({"status": status})

    @staticmethod
    def get_online_responders_from_district(district: str):
        responders_ref = db.collection("responders")
        query = responders_ref.where(
            filter=firestore.FieldFilter("district", "==", district)
        )
        query = query.where(filter=firestore.FieldFilter("is_online", "==", True))
        return [{"id": doc.id, **doc.to_dict()} for doc in query.get()]

    @staticmethod
    def record_responder_response(sos_id: str, responder_id: str, response: str):
        sos_ref = db.collection("sos_messages").document(sos_id)
        sos_response = {
            "responder_id": responder_id,
            "response": response,
            "timestamp": int(time.time()),
        }
        sos_ref.collection("responses").add(sos_response)

        if response == "accept":
            sos_ref.update(
                {"accepted_by": responder_id, "accepted_at": int(time.time())}
            )
