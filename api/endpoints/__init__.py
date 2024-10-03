from api.endpoints.sos import router as sos_router
from api.endpoints.responder import router as responder_router
from api.endpoints.status import router as status_router

__all__ = ["sos_router", "responder_router", "status_router"]
