from fastapi import APIRouter, Depends, HTTPException
from models.schemas import BaseResponse
from api.dependencies import verify_firebase_token
from firebase_admin import firestore

router = APIRouter()

db = firestore.client()


@router.get("/{sos_id}/status", response_model=BaseResponse)
async def get_sos_status(sos_id: str, token: dict = Depends(verify_firebase_token)):
    sos_ref = db.collection("sos_messages").document(sos_id)
    sos_doc = sos_ref.get()

    if not sos_doc.exists:
        raise HTTPException(status_code=404, detail="SOS not found")

    sos_data = sos_doc.to_dict()
    user_data = sos_data["user_ref"].get().to_dict()

    full_sos_data = {**sos_data}
    full_sos_data.update(user_data)
    del full_sos_data["user_ref"]

    return BaseResponse(
        status="success", message="SOS status retrieved", data=full_sos_data
    )
