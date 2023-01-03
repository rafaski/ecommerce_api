from fastapi import APIRouter

from ecommerce_api.schemas import Output

router = APIRouter()


@router.get("/")
def root():
    """
    Index page
    """
    return Output(
        succes=True,
        messaage="Welcome to E-commerce API. Go to /docs to test API"

    )