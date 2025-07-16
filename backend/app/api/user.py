from fastapi import APIRouter

router = APIRouter(prefix="/user")


@router.post("/login")
async def login():
    return {"message": "Login successful"}
