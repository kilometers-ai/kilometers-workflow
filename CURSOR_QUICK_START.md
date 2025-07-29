# 🚀 Cursor Prompt for First-Time Project Setup

Copy and paste this into Cursor's AI chat:

---

I need to set up and run the kilometers-workflow project for the first time. This is an AI Agent Workflow System using CrewAI and LangGraph.

Please help me:

1. **Setup Python Environment**
   - Navigate to `/projects/kilometers.ai/kilometers-workflow/`
   - Create virtual environment
   - Activate it
   - Install dependencies

2. **Configure Environment**
   - Create .env from the template
   - Add my OpenAI API key
   - Verify all required env vars are set

3. **Start Docker Services**
   - Check docker-compose.yml
   - Start PostgreSQL, Redis containers
   - Verify they're running

4. **Run the API Server**
   - Start FastAPI server
   - Test the health endpoint
   - Check WebSocket connection

5. **Execute Test Workflow**
   - Run examples/run_workflow.py
   - Verify market validation agent works
   - Check output and artifacts

Show me the exact commands for each step and help debug any errors. Let's start with step 1!

Key files:
- setup script: `scripts/setup.sh`
- API server: `services/api-gateway/main.py`
- example: `examples/run_workflow.py`
- docker config: `docker-compose.yml`

Current directory: `/projects/kilometers.ai/kilometers-workflow/`

---

## Alternative Quick Start Prompt

If you want Cursor to do everything automatically:

---

@workspace Set up and run the kilometers-workflow project:

1. Make scripts/setup.sh executable and run it
2. Create .env file and remind me to add OpenAI API key
3. Start docker-compose services (postgres, redis)
4. Install Python dependencies in a virtual environment
5. Run the FastAPI server
6. Execute examples/run_workflow.py to test

Fix any errors that come up and ensure everything runs successfully. Current dir: /projects/kilometers.ai/kilometers-workflow/

---