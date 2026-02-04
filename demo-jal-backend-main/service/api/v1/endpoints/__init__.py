# FILE: /fastapi-backend/fastapi-backend/app/api/v1/endpoints/__init__.py
from fastapi import APIRouter

router = APIRouter()

from .routes import generate_answer

router.add_api_route("/generate_answer", generate_answer, methods=["POST"])