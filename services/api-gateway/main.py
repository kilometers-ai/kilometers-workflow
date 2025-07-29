"""
FastAPI Gateway for the SDLC Workflow System
"""

import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import BackgroundTasks, FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ...orchestration.workflow_engine.sdlc_workflow import SDLCWorkflowEngine
from ...shared.models.workflow import StageStatus, WorkflowState


class WorkflowRequest(BaseModel):
    """Request to start a new workflow"""

    project_idea: str
    metadata: Optional[Dict[str, Any]] = None


class WorkflowResponse(BaseModel):
    """Response from workflow operations"""

    workflow_id: str
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None


class APIGateway:
    """Main API Gateway for the workflow system"""

    def __init__(self):
        self.app = FastAPI(
            title="SDLC AI Workflow API",
            description="API for orchestrating AI-driven software development lifecycle",
            version="0.1.0",
        )
        self.workflow_engine = SDLCWorkflowEngine()
        self.active_workflows: Dict[str, WorkflowState] = {}
        self.websocket_connections: Dict[str, WebSocket] = {}

        self._setup_middleware()
        self._setup_routes()

    def _setup_middleware(self):
        """Configure middleware"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _setup_routes(self):
        """Setup API routes"""

        @self.app.get("/")
        async def root():
            return {"message": "SDLC AI Workflow API", "status": "active"}

        @self.app.post("/workflows", response_model=WorkflowResponse)
        async def create_workflow(request: WorkflowRequest, background_tasks: BackgroundTasks):
            """Create and start a new workflow"""
            workflow_id = str(uuid.uuid4())

            # Create workflow state
            workflow_state = WorkflowState(
                workflow_id=workflow_id,
                project_idea=request.project_idea,
                current_stage="initializing",
                global_context=request.metadata or {},
            )

            self.active_workflows[workflow_id] = workflow_state

            # Start workflow in background
            background_tasks.add_task(self._run_workflow, workflow_id, request.project_idea)

            return WorkflowResponse(
                workflow_id=workflow_id,
                status="started",
                message=f"Workflow started for: {request.project_idea}",
                data={"created_at": workflow_state.created_at.isoformat()},
            )

        @self.app.get("/workflows/{workflow_id}", response_model=WorkflowResponse)
        async def get_workflow_status(workflow_id: str):
            """Get current status of a workflow"""
            if workflow_id not in self.active_workflows:
                raise HTTPException(status_code=404, detail="Workflow not found")

            workflow = self.active_workflows[workflow_id]

            return WorkflowResponse(
                workflow_id=workflow_id,
                status=workflow.current_stage,
                message="Workflow status retrieved",
                data={
                    "current_stage": workflow.current_stage,
                    "completed_stages": [
                        s.stage_name for s in workflow.stages if s.status == StageStatus.COMPLETED
                    ],
                    "artifacts_count": len(workflow.get_all_artifacts()),
                    "updated_at": workflow.updated_at.isoformat(),
                },
            )

        @self.app.get("/workflows")
        async def list_workflows():
            """List all workflows"""
            workflows = []
            for wf_id, wf_state in self.active_workflows.items():
                workflows.append(
                    {
                        "workflow_id": wf_id,
                        "project_idea": wf_state.project_idea,
                        "current_stage": wf_state.current_stage,
                        "created_at": wf_state.created_at.isoformat(),
                    }
                )

            return {"workflows": workflows, "total": len(workflows)}

        @self.app.get("/workflows/{workflow_id}/artifacts")
        async def get_workflow_artifacts(workflow_id: str):
            """Get all artifacts from a workflow"""
            if workflow_id not in self.active_workflows:
                raise HTTPException(status_code=404, detail="Workflow not found")

            workflow = self.active_workflows[workflow_id]
            return {"workflow_id": workflow_id, "artifacts": workflow.get_all_artifacts()}

        @self.app.websocket("/ws/{workflow_id}")
        async def websocket_endpoint(websocket: WebSocket, workflow_id: str):
            """WebSocket endpoint for real-time workflow updates"""
            await websocket.accept()
            self.websocket_connections[workflow_id] = websocket

            try:
                while True:
                    # Keep connection alive
                    await asyncio.sleep(1)
            except Exception:
                pass
            finally:
                if workflow_id in self.websocket_connections:
                    del self.websocket_connections[workflow_id]

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "active_workflows": len(self.active_workflows),
            }

    async def _run_workflow(self, workflow_id: str, project_idea: str):
        """Run a workflow asynchronously"""
        try:
            async for event in self.workflow_engine.run_workflow(project_idea, workflow_id):
                # Update workflow state
                if workflow_id in self.active_workflows:
                    # Process event and update state
                    await self._process_workflow_event(workflow_id, event)

                    # Send WebSocket update if connected
                    if workflow_id in self.websocket_connections:
                        await self._send_websocket_update(workflow_id, event)

        except Exception as e:
            # Handle workflow errors
            if workflow_id in self.active_workflows:
                self.active_workflows[workflow_id].current_stage = "failed"
                await self._send_websocket_update(
                    workflow_id, {"error": str(e), "stage": "workflow_error"}
                )

    async def _process_workflow_event(self, workflow_id: str, event: Dict[str, Any]):
        """Process workflow events and update state"""
        workflow = self.active_workflows.get(workflow_id)
        if not workflow:
            return

        # Update current stage based on event
        for key, value in event.items():
            if "current_stage" in value:
                workflow.current_stage = value["current_stage"]

            # Add more event processing logic here

    async def _send_websocket_update(self, workflow_id: str, data: Dict[str, Any]):
        """Send update via WebSocket"""
        websocket = self.websocket_connections.get(workflow_id)
        if websocket:
            try:
                await websocket.send_json(
                    {
                        "workflow_id": workflow_id,
                        "timestamp": datetime.utcnow().isoformat(),
                        "data": data,
                    }
                )
            except Exception:
                # Remove failed connection
                del self.websocket_connections[workflow_id]


# Create the FastAPI app instance
gateway = APIGateway()
app = gateway.app

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
