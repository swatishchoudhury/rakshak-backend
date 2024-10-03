from firebase_admin import messaging
from typing import Dict, Any


class NotificationService:
    @staticmethod
    def send_help_call(
        responder: Dict[str, Any],
        sos_data: Dict[str, Any],
        user_data: Dict[str, Any],
        sos_id: str,
    ) -> bool:
        try:
            help_call_data = {
                "sos_id": sos_id,
                "coordinates": sos_data["coordinates"],
                "timestamp": str(sos_data["timestamp"]),
                "user_name": user_data.get("name"),
                "blood_group": user_data.get("blood_group"),
                "emergency_contacts": ",".join(user_data.get("emergency_contacts", [])),
            }

            message = messaging.Message(
                data=help_call_data,
                token=responder["fcm_token"],
                notification=messaging.Notification(
                    title="New SOS Alert",
                    body=f"SOS from {user_data.get('name')}. Blood Group: {user_data.get('blood_group')}",
                ),
                android=messaging.AndroidConfig(
                    priority="high",
                    notification=messaging.AndroidNotification(
                        icon="notification_icon", color="#f45342"
                    ),
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(badge=1, sound="default")
                    )
                ),
            )

            response = messaging.send(message)
            print(
                f"Successfully sent message to responder {responder['id']}: {response}"
            )
            return True
        except Exception as e:
            print(f"Error sending FCM message to responder {responder['id']}: {e}")
            return False
