import logging

from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from schemas import ProcessRequest, AgentResponse
from Orchestrator import AgentOrchestratorController
from Orchestrator.stubs import StubExtractionService, StubStateService


logger = logging.getLogger("uv-logger")

agent_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"],
)


@agent_router.post("/agent/process")
async def process_agent_request(process_request: ProcessRequest):
    """
    Main agent endpoint.
    Accepts a user message + current conversation state,
    runs the agent pipeline, and returns an AgentResponse.
    """

    logger.info("Received agent request: %s", process_request.message[:100])

    orchestrator_client = AgentOrchestratorController(
    extraction_service=StubExtractionService(),
    state_service=StubStateService()
)

    try:
        result = await orchestrator_client.process(
            message=process_request.message,
            current_state=process_request.current_state,
        )

        logger.info("Agent request processed: action=%s", result.next_action.value)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "result": result.model_dump()
                },
        )

    except ValidationError as e:
        logger.warning("State validation failed: %s", e.error_count())
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        )

    except Exception as e:
        logger.error("Agent processing error: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent processing error: {str(e)}",
        )