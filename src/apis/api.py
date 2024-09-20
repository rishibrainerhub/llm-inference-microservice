from fastapi import APIRouter, Depends
from schemas.reviews import Review, BatchReviews
from services.analyze import AnalyzeService

router = APIRouter()


@router.post("/analyze_review")
async def analyze_review(
    review: Review, service: AnalyzeService = Depends(AnalyzeService)
):
    return await service.analyze_review(review)


@router.post("/analyze_batch")
async def analyze_batch(
    batch: BatchReviews, service: AnalyzeService = Depends(AnalyzeService)
):
    return await service.analyze_batch(batch)


@router.get("/metrics")
async def metrics():
    return generate_latest()
