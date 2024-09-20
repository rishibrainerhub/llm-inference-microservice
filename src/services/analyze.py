from database.database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from pipeline.customIn_ference_pipeline import CustomInferencePipeline
from database.models import ReviewResult
from concurrent.futures import ThreadPoolExecutor
import asyncio
from typing import List, Dict, Any


class AnalyzeService:
    def __init__(
        self,
        db: Session = Depends(get_db),
        pipeline: CustomInferencePipeline = Depends(CustomInferencePipeline),
    ) -> None:
        self.db = db
        self.pipeline = pipeline

    async def analyze_review(self, review) -> ReviewResult:
        result = self.pipeline(review.text)
        await self.store_result(self.db, result)
        return result

    async def analyze_batch(self, batch) -> list:
        with ThreadPoolExecutor() as executor:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                executor, self.batch_process, self.pipeline, batch.reviews
            )

        await asyncio.gather(
            *[self.store_result(self.db, result) for result in results]
        )

        return results

    @staticmethod
    async def store_result(db: Session, result: Dict[str, Any]) -> None:
        """
        Store the result in the database.

        Args:
            db (Session): The database session.
            result (Dict[str, Any]): The result to store.

        Returns:
            None
        """

        try:
            new_result = ReviewResult(
                original_text=result["original_text"],
                sentiment=result["sentiment"],
                confidence=result["confidence"],
                entities=result["entities"],
                text_length=result["text_length"],
                contains_product_mention=result["contains_product_mention"],
            )
            db.add(new_result)
            db.commit()
        except Exception as e:
            db.rollback()

    @staticmethod
    def batch_process(
        pipeline: CustomInferencePipeline, texts: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Process a batch of texts using the custom inference pipeline.

        Args:
            pipeline (CustomInferencePipeline): The initialized pipeline.
            texts (List[str]): A list of texts to process.

        Returns:
            List[Dict[str, Any]]: A list of processed results.
        """
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(pipeline, texts))
        return results
