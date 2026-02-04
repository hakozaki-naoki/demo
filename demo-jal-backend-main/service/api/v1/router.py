from fastapi import APIRouter
from service.api.v1.endpoints.routes import generate_answer

router = APIRouter()

router.add_api_route("/generate_answer", generate_answer, methods=["POST"])