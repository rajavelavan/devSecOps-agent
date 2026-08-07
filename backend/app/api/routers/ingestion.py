from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.core.queue import mock_sqs_queue
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/mock/sqs/push")
async def mock_sqs_push(payload: Dict[str, Any]):
    """
    Simulates AWS EventBridge pushing a message to an SQS queue.
    The background worker will pick this up from the queue.
    """
    logger.info("Received mock SQS message push")
    try:
        await mock_sqs_queue.put(payload)
        return {"status": "success", "message": "Message enqueued successfully"}
    except Exception as e:
        logger.error(f"Failed to enqueue message: {e}")
        raise HTTPException(status_code=500, detail="Failed to enqueue message")
