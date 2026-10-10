from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
def success_response(message: str, data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }

    return JSONResponse(status_code=200, content=jsonable_encoder(content))