# kilometers-workflow

## 🚀 AI Agent Workflow System for SDLC Automation

A customizable workflow builder that orchestrates AI agents through the entire software development lifecycle using CrewAI and LangGraph.

### Quick Start with Cursor

Using Cursor AI? Check these prompts:
- **First Time Setup**: See `CURSOR_MASTER_PROMPT.md`
- **Quick Commands**: See `CURSOR_QUICK_START.md`
- **Troubleshooting**: See `CURSOR_TROUBLESHOOTING.md`

### Manual Setup

```bash
# 1. Make setup script executable
chmod +x scripts/setup.sh

# 2. Run setup
./scripts/setup.sh

# 3. Configure environment
# Edit .env and add your OPENAI_API_KEY

# 4. Start services
docker-compose up -d

# 5. Run API
source venv/bin/activate
uvicorn services.api_gateway.main:app --reload

# 6. Test workflow
python examples/run_workflow.py
```

### Architecture

- **Orchestration**: LangGraph for complex workflows
- **Agents**: CrewAI for rapid prototyping
- **API**: FastAPI with WebSocket support
- **Storage**: PostgreSQL with pgvector
- **Queue**: Redis for async tasks
- **Monitoring**: Phoenix/AgentOps integration

### Documentation

- Task Breakdown: `docs/TASK_BREAKDOWN.md`
- Architecture: `ARCHITECTURE_SUMMARY.md`
- Scaffolding Guide: `docs/guides/QUICK_SCAFFOLDING.md`