from fastapi import FastAPI
from api.endpoints import sos, responder, status

__version__ = "0.7.5"

app = FastAPI(
    title="Rakshak API",
    description="Emergency response system API for connecting people in need with responders",
    version=__version__,
)

app.include_router(sos.router, prefix="/smsapi", tags=["SOS"])
app.include_router(responder.router, prefix="/responder", tags=["Responder"])
app.include_router(status.router, prefix="/sos", tags=["Status"])


@app.get("/")
async def read_root():
    return {
        "status": "success",
        "message": "Rakshak",
        "data": {"info": "This is the root endpoint for RakshakAPI."},
    }
