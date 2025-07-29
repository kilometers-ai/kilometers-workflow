# Cursor AI Assistant Prompt: First-Time Setup & Run

## Project Context
I'm working on the kilometers-workflow project, an AI Agent Workflow System for SDLC automation using CrewAI and LangGraph. The project is located at `/projects/kilometers.ai/kilometers-workflow/`.

## Task
Help me set up and run this project for the first time. I need to:
1. Install all dependencies
2. Configure environment variables
3. Start the required services
4. Run a test workflow to verify everything works

## Current Status
- The project structure is already created
- I have Python, Docker, and Docker Compose installed
- I haven't run the project yet
- I need to add my OpenAI API key

## Step-by-Step Instructions Needed

### 1. Environment Setup
- Create and activate a Python virtual environment
- Install all dependencies from requirements.txt
- Create a .env file with proper API keys

### 2. Docker Services
- Verify docker-compose.yml is correct
- Start PostgreSQL, Redis, and other services
- Check that all containers are running

### 3. Run First Workflow
- Start the FastAPI server
- Execute the example workflow script
- Verify the market validation agent works

### 4. Troubleshooting
- Handle any import errors
- Fix any missing dependencies
- Resolve any Docker networking issues

## Expected Outcomes
- All services running successfully
- API accessible at http://localhost:8000
- Successful execution of a test workflow
- Market validation agent produces output

## Code Context
Key files to work with:
- `scripts/setup.sh` - Setup script
- `docker-compose.yml` - Service definitions
- `services/api-gateway/main.py` - API server
- `examples/run_workflow.py` - Example workflow
- `agents/market-validation/market_validation_agent.py` - First agent to test

Please guide me through each step, showing the exact commands to run and helping me verify each step succeeds before moving to the next. If we encounter errors, help me debug and fix them.

Let's start with making the setup script executable and running it!