from fastapi import APIRouter

from ecommerce_api.schemas import Output

router = APIRouter()


@router.get("/")
def index():
    """
    Index page
    """
    return Output(
        success=True,
        message="Welcome to e-commerce API. Go to /docs to test API."
    )
