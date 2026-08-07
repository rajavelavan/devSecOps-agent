import asyncio
import logging
from app.core.queue import mock_sqs_queue
from app.models.eventbridge import EventBridgeEvent
from pydantic import ValidationError
from app.agent.graph import agent_graph
from app.agent.state import AgentState

logger = logging.getLogger(__name__)

async def process_event(event: EventBridgeEvent):
    logger.info(f"Processing EventBridge Event: {event.id} from {event.source}")
    for finding in event.detail.findings:
        logger.info(f"Analyzing Security Hub Finding: {finding.Title} ({finding.Id})")
        
        resource_id = finding.Resources[0].Id if finding.Resources else "unknown"
        
        initial_state: AgentState = {
            "alert_event_type": event.source,
            "alert_event_name": finding.Title,
            "alert_resource_id": resource_id,
            "alert_severity": finding.Severity.Label,
            "alert_details": finding.Description,
            "retry_count": 0,
            "messages": [],
            "threat_classification": None,
            "threat_score": None,
            "remediation_script": None,
            "remediation_valid": None,
            "execution_status": None,
            "execution_output": None
        }
        
        # Spin up a task so we don't block the queue processing
        asyncio.create_task(run_agent(initial_state, finding.Id))

async def run_agent(initial_state: AgentState, finding_id: str):
    logger.info(f"Starting agent workflow for finding {finding_id}")
    try:
        final_state = await agent_graph.ainvoke(initial_state)
        logger.info(f"Completed agent workflow for finding {finding_id}. Status: {final_state.get('execution_status')}")
    except Exception as e:
        logger.error(f"Error executing agent workflow for finding {finding_id}: {e}")

async def sqs_polling_worker():
    logger.info("Starting background SQS polling worker...")
    while True:
        try:
            message_payload = await mock_sqs_queue.get()
            logger.debug(f"Received raw message from queue")
            
            try:
                event = EventBridgeEvent.model_validate(message_payload)
                await process_event(event)
            except ValidationError as e:
                logger.error(f"Message failed schema validation: {e}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
            finally:
                mock_sqs_queue.task_done()
                
        except asyncio.CancelledError:
            logger.info("SQS polling worker shutting down...")
            break
        except Exception as e:
            logger.error(f"Unexpected error in SQS worker: {e}")
            await asyncio.sleep(5)
