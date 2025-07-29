"""
Example: Running a complete SDLC workflow
"""

import asyncio

from dotenv import load_dotenv

from agents.market_validation.market_validation_agent import MarketValidationAgent
from orchestration.workflow_engine.sdlc_workflow import SDLCWorkflowEngine

# Load environment variables
load_dotenv()


async def run_example_workflow():
    """Example of running the SDLC workflow"""

    # Project idea to develop
    project_idea = "Build a simpler Jira/Linear work tracking platform with AI automation"

    print(f"🚀 Starting SDLC workflow for: {project_idea}")
    print("-" * 60)

    # Option 1: Run individual agent
    print("\n📊 Running Market Validation Agent...")
    market_agent = MarketValidationAgent()
    result = await market_agent.execute({"project_idea": project_idea})

    if result.success:
        print("✅ Market validation completed!")
        print(f"Viability: {result.output.get('market_validation', {}).get('project_viability')}")
        print(
            f"Score: {result.output.get('market_validation', {}).get('market_opportunity_score')}"
        )
    else:
        print("❌ Market validation failed:", result.errors)

    # Option 2: Run complete workflow
    print("\n🔄 Running complete SDLC workflow...")
    workflow_engine = SDLCWorkflowEngine()

    workflow_events = []
    async for event in workflow_engine.run_workflow(project_idea):
        workflow_events.append(event)
        print(f"Stage: {event}")

    print("\n✅ Workflow completed!")
    print(f"Total stages processed: {len(workflow_events)}")


async def test_api_gateway():
    """Test the API gateway"""
    import httpx

    # Make sure the API is running first
    async with httpx.AsyncClient() as client:
        # Create a new workflow
        response = await client.post(
            "http://localhost:8000/workflows",
            json={"project_idea": "Build an AI-powered code review tool"},
        )

        if response.status_code == 200:
            data = response.json()
            workflow_id = data["workflow_id"]
            print(f"✅ Workflow created: {workflow_id}")

            # Check status
            status_response = await client.get(f"http://localhost:8000/workflows/{workflow_id}")
            print(f"Status: {status_response.json()}")


if __name__ == "__main__":
    # Run the example
    asyncio.run(run_example_workflow())

    # Uncomment to test API
    # asyncio.run(test_api_gateway())
