from fastapi import APIRouter

router = APIRouter(prefix="user", tags=["user"])


@router.post("/login")
async def login():
    return {"message": "Login successful"}
