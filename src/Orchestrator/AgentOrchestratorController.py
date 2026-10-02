"""
Agent orchestrator — the central pipeline of AI1.

Responsibilities:
- Validate incoming state
- Delegate extraction to AI3 (via ExtractionServicePort)
- Delegate state patching to AI3 (via StateServicePort)
- Select the next action
- Build the assistant response

Does NOT contain:
- Extraction / NLP logic (AI3)
- State merge algorithm (AI3)
- Missing-fields detection (AI3)
- Backend tool calls (future milestone)
"""

from schemas.state import ConversationState
from schemas.AgentResponse import AgentResponse
from enums.AgentAction import AgentAction

from Orchestrator.ports import ExtractionServicePort, StateServicePort # temprory

from Orchestrator.ActionSelector import ActionSelector
from Orchestrator.MissingFieldsPolicy import MissingFieldsPolicy

import logging

class AgentOrchestratorController:

    def __init__(
        self,
        extraction_service: ExtractionServicePort, # temprory
        state_service: StateServicePort, # temprory
    ):
        
        self._extraction_service = extraction_service
        self._state_service = state_service

        self._missing_fields_policy = MissingFieldsPolicy()
        self._action_selector = ActionSelector()

        self.logger = logging.getLogger(__name__)

    async def process(self, message: str, current_state: dict) -> AgentResponse:
        """
        Main agent pipeline.

        message + current_state
            → validate state
            → extract 
            → apply patch 
            → select action
            → build response
        """

        # ── Step 1: Validate incoming state ───────────────────────────
        state = ConversationState.model_validate(current_state)
        self.logger.info("State validated successfully")


        # ── Step 2: Extract intent + requirements via AI3 ─────────────
        extraction = await self._extraction_service.extract(
            message=message,
            current_state=state,
        ) 
        if not extraction:
            self.logger.warning("Extraction failed")
            raise ValueError("Extraction failed")
        
        self.logger.info(
            "Extraction complete: intent=%s, confidence=%.2f, missing=%s",
            extraction.intent, extraction.confidence, extraction.missing_fields,
        )

        ## from extraction requirements, we can determine the next action and build the assistant message,
        ## next action based on missing fields, and assistant message based on missing fields policy


        # ── Step 3: Apply state patch via AI3 ─────────────────────────
        updated_state = self._state_service.apply_patch(
            current_state=state,
            state_patch=extraction.state_patch,
            intent=extraction.intent,
        )
        
        self.logger.info("State patched via StateService")


        # ── Step 4: Select next action ────────────────────────────────
        action = self._action_selector.select(
            missing_fields=extraction.missing_fields,
        )
        if not action:
            self.logger.warning("Action selection failed")
            raise ValueError("Action selection failed")
        
        self.logger.info("Selected action: %s", action.value)


        # ── Step 5: Build assistant message ───────────────────────────
        if action == AgentAction.ASK_MISSING_INFORMATION:
            assistant_message = self._missing_fields_policy.build_question(
                extraction.missing_fields,
            )

        elif action == AgentAction.SEARCH_ROOMS:
            # No actual search yet — future milestone
            assistant_message = ""

        else:
            assistant_message = ""


        self.logger.info("Pipeline complete: action=%s", action.value)

        return AgentResponse(
            assistant_message=assistant_message,
            next_action=action,
            state_patch=extraction.state_patch,
            missing_fields=extraction.missing_fields,
        )