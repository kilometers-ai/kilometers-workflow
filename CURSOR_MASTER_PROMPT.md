# 🎯 Master Cursor Prompt for kilometers-workflow

Copy this entire prompt into Cursor:

---

## Project: AI Agent Workflow System (kilometers-workflow)

I need to run the kilometers-workflow project for the first time. This is an AI-powered SDLC automation system using CrewAI, LangGraph, and FastAPI.


### Phase 1: Initial Setup
```bash

# Make setup script executable
chmod +x scripts/setup.sh

# Run setup (creates venv, installs deps, etc.)
./scripts/setup.sh
```

### Phase 2: Environment Configuration
After setup completes, I need to:
1. Edit `.env` file and add my OpenAI API key
2. Verify all required environment variables are present
3. Source the .env file

### Phase 3: Start Services
```bash
# Start Docker services (PostgreSQL, Redis)
docker-compose up -d redis postgres

# Verify services are running
docker-compose ps
```

### Phase 4: Run API Server
```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
uvicorn services.api_gateway.main:app --reload --host 0.0.0.0 --port 8000
```

### Phase 5: Test Workflow
In a new terminal:
```bash
# Activate venv
source venv/bin/activate

# Run example workflow
python examples/run_workflow.py
```

### Expected Results:
- API running at http://localhost:8000
- Swagger docs at http://localhost:8000/docs
- Example workflow completes successfully
- Market validation agent produces output

### If Issues Occur:
1. **Import Errors**: Check PYTHONPATH and __init__.py files
2. **Connection Errors**: Verify Docker networking and .env settings
3. **Missing Modules**: Install with pip and update requirements.txt
4. **API Errors**: Check logs with --log-level debug

### Key Files to Monitor:
- `services/api-gateway/main.py` - API server
- `orchestration/workflow-engine/sdlc_workflow.py` - Workflow engine
- `agents/market-validation/market_validation_agent.py` - First agent
- `examples/run_workflow.py` - Test script

Please execute each phase sequentially, showing me the output and helping me resolve any errors before proceeding to the next phase.

**Important**: After each command, verify success before moving forward. If we encounter errors, let's debug them immediately.

Let's begin with Phase 1!

---

## 🚀 Quick Alternative (One Command)

Or use this for Cursor to handle everything:

---

@workspace I need to run kilometers-workflow for the first time. Execute these in order:

```bash
chmod +x scripts/setup.sh && ./scripts/setup.sh
# Wait for completion
echo "⚠️ ADD YOUR OPENAI_API_KEY TO .env FILE NOW!"
# After user confirms
docker-compose up -d redis postgres
source venv/bin/activate
python -m pytest # Quick test
uvicorn services.api_gateway.main:app --reload &
sleep 5
python examples/run_workflow.py
```

Debug any errors and ensure the workflow runs successfully.

---