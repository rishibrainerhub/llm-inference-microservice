# LLM Inference Microservice

This project implements a microservice for sentiment analysis on product reviews using a Large Language Model (LLM). It includes advanced pre-processing and post-processing steps, and integrates with a PostgreSQL database for storing analysis results.

## Features

- Custom inference pipeline for sentiment analysis
- FastAPI web service for easy integration
- Single review and batch processing endpoints
- PostgreSQL database integration for storing results
- Alembic for database migration
- Docker Compose setup for easy deployment

## Prerequisites

- Docker
- Docker Compose

## Project Structure

```
.
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── README.MD
├── requirements.txt
└── src
    ├── alembic
    │   ├── env.py
    │   ├── README
    │   ├── script.py.mako
    │   └── versions
    │       ├── 125d4c2867c1_initial_migration.py
    ├── apis
    │   ├── api.py
    ├── database
    │   ├── database.py
    │   ├── models.py
    ├── pipeline
    │   ├── customIn_ference_pipeline.py
    ├── schemas
    │   └── reviews.py
    ├── services
    │   ├── analyze.py
    ├── __init__.py
    ├── main.py
```

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/rishibrainerhub/llm-inference-microservice.git
   cd llm-inference-microservice
   ```

2. Build and start the services:
   ```bash
   docker-compose up --build
   ```

3. The service will be available at `http://localhost:8000`

## API Endpoints

### 1. Analyze Single Review

- **URL**: `/analyze_review`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "text": "Your review text here"
  }
  ```
- **Response**: JSON object with analysis results

### 2. Analyze Batch of Reviews

- **URL**: `/analyze_batch`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "reviews": ["Review 1 text", "Review 2 text", ...]
  }
  ```
- **Response**: Array of JSON objects with analysis results

## Configuration

Environment variables can be set in the `docker-compose.yml` file:

- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_NAME`: PostgreSQL database name
- `DB_HOST`: PostgreSQL host
- `DATABASE_URL`: DataBase url

## Database Schema

The service uses a PostgreSQL database with the following schema:

```python
class ReviewResult(Base):
    __tablename__ = "review_results"

    review_id = Column(Integer, primary_key=True, index=True)
    original_text = Column(String)
    sentiment = Column(String)
    confidence = Column(Float)
    entities = Column(ARRAY(String))
    text_length = Column(Integer)
    contains_product_mention = Column(Boolean)
    processed_at = Column(TIMESTAMP)
```

## Custom Inference Pipeline

The custom inference pipeline (`custom_inference_pipeline.py`) includes the following steps:

1. Text preprocessing (HTML removal, special character removal)
2. Sentiment analysis using a pre-trained LLM
3. Named entity extraction
4. Result postprocessing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.