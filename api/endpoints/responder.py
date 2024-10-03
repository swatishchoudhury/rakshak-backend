from fastapi import APIRouter, Depends
from models.schemas import ResponderResponse, BaseResponse
from api.dependencies import verify_firebase_token
from services.firebase_service import FirebaseService

router = APIRouter()


@router.post("/response", response_model=BaseResponse)
async def responder_response(
    response: ResponderResponse, token: dict = Depends(verify_firebase_token)
):
    responder_id = token["uid"]
    FirebaseService.record_responder_response(
        response.sos_id, responder_id, response.response
    )

    return BaseResponse(
        status="success",
        message="Response recorded successfully",
        data={"responder_id": responder_id, "response": response.response},
    )
