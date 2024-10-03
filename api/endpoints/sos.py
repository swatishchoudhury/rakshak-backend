from fastapi import APIRouter, Depends, HTTPException, status
from models.schemas import SOSData, BaseResponse
from api.dependencies import verify_api_key
from services.firebase_service import FirebaseService
from services.location_service import LocationService
from services.notification_service import NotificationService
from utils.helpers import decode_sos_text

router = APIRouter()


@router.post("/sos", response_model=BaseResponse)
async def receive_sos(sos_data: SOSData, api_key: str = Depends(verify_api_key)):
    decoded_sos_data = decode_sos_text(sos_data.sos_text)

    user_doc = FirebaseService.get_user_by_email(decoded_sos_data["email"])
    if not user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found",
        )

    sos_data_to_store = {
        "coordinates": decoded_sos_data["coordinates"],
        "timestamp": int(decoded_sos_data["timestamp"]),
        "phone_number": sos_data.phone_number,
        "status": "pending",
    }

    sos_ref = FirebaseService.store_sos(sos_data_to_store, user_doc.id)
    district = LocationService.get_district(decoded_sos_data["coordinates"])
    responders = FirebaseService.get_online_responders_from_district(district)

    if not responders:
        FirebaseService.update_sos_status(sos_ref[1].id, "no_responders")
        return BaseResponse(
            status="partial_success",
            message="SOS received, but no responders available in the area",
            data={"sos_id": sos_ref[1].id},
        )

    sorted_responders = LocationService.sort_responders_by_distance(
        responders, decoded_sos_data["coordinates"]
    )
    closest_responders = sorted_responders[:3]

    notification_sent = any(
        NotificationService.send_help_call(
            responder, sos_data_to_store, user_doc.to_dict(), sos_ref[1].id
        )
        for responder in closest_responders
    )

    if notification_sent:
        FirebaseService.update_sos_status(sos_ref[1].id, "notified")
        return BaseResponse(
            status="success",
            message="SOS received and responders notified",
            data={"sos_id": sos_ref[1].id},
        )
    else:
        FirebaseService.update_sos_status(sos_ref[1].id, "notification_failed")
        return BaseResponse(
            status="partial_success",
            message="SOS received, but failed to notify responders",
            data={"sos_id": sos_ref[1].id},
        )
