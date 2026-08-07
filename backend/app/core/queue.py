import asyncio

# Global queue to simulate SQS locally
mock_sqs_queue: asyncio.Queue = asyncio.Queue()
