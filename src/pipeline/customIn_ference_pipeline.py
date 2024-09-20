from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from typing import List, Dict, Any
import re
import spacy
from concurrent.futures import ThreadPoolExecutor


class CustomInferencePipeline:
    def __init__(
        self, model_name: str = "distilbert-base-uncased-finetuned-sst-2-english"
    ):
        """
        Initialize the custom inference pipeline.

        Args:
            model_name (str): The name of the pre-trained model to use.
        """
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, clean_up_tokenization_spaces=False
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_pipeline = pipeline(
            "sentiment-analysis", model=self.model, tokenizer=self.tokenizer
        )

    def preprocess(self, text: str) -> str:
        """
        Preprocess the input text.

        Args:
            text (str): The input text to preprocess.

        Returns:
            str: The preprocessed text.
        """
        # Remove HTML tags
        text = re.sub(r"<[^>]+>", "", text)
        # Remove special characters and digits
        text = re.sub(r"[^a-zA-Z\s]", "", text)
        # Convert to lowercase
        text = text.lower()
        return text

    def extract_entities(self, text: str) -> List[str]:
        """
        Extract named entities from the text.

        Args:
            text (str): The input text to extract entities from.

        Returns:
            List[str]: A list of extracted entities.
        """
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents]

    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze the sentiment of the given text.

        Args:
            text (str): The input text to analyze.

        Returns:
            Dict[str, Any]: A dictionary containing the sentiment analysis results.
        """
        result = self.sentiment_pipeline(text)[0]
        return {"label": result["label"], "score": result["score"]}

    def postprocess(
        self, text: str, sentiment: Dict[str, Any], entities: List[str]
    ) -> Dict[str, Any]:
        """
        Postprocess the results.

        Args:
            text (str): The original input text.
            sentiment (Dict[str, Any]): The sentiment analysis results.
            entities (List[str]): The extracted entities.

        Returns:
            Dict[str, Any]: A dictionary containing the postprocessed results.
        """
        return {
            "original_text": text,
            "sentiment": sentiment["label"],
            "confidence": sentiment["score"],
            "entities": entities,
            "text_length": len(text.split()),
            "contains_product_mention": any(
                entity.lower() in ["product", "item", "purchase"] for entity in entities
            ),
        }

    def __call__(self, text: str) -> Dict[str, Any]:
        """
        Run the full inference pipeline on the input text.

        Args:
            text (str): The input text to process.

        Returns:
            Dict[str, Any]: A dictionary containing the final results.
        """
        preprocessed_text = self.preprocess(text)

        with ThreadPoolExecutor() as executor:
            sentiment_future = executor.submit(
                self.analyze_sentiment, preprocessed_text
            )
            entities_future = executor.submit(self.extract_entities, preprocessed_text)

            sentiment = sentiment_future.result()
            entities = entities_future.result()

        return self.postprocess(text, sentiment, entities)
