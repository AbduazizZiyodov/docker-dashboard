from fastapi import APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()


@router.get("/")
async def root() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})
