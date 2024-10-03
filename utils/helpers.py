import base64
import json
from fastapi import HTTPException, status


def decode_sos_text(sos_text: str) -> dict:
    try:
        encoded_part = sos_text.replace("Rakshak ", "")
        decoded_bytes = base64.b64decode(encoded_part)
        decoded_str = decoded_bytes.decode("utf-8")
        return json.loads(decoded_str)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to decode SOS text: {str(e)}",
        )
