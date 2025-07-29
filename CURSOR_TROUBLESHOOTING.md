# 🛠️ Cursor Troubleshooting Prompts

## For Common Setup Issues

### Python Import Errors
```
I'm getting import errors when running the kilometers-workflow project. The error is: [PASTE ERROR HERE]

Project structure is in /projects/kilometers.ai/kilometers-workflow/
Please help me:
1. Check if all __init__.py files exist
2. Verify PYTHONPATH is set correctly
3. Ensure virtual environment is activated
4. Fix any circular imports
```

### Docker Connection Issues
```
Docker services started but API can't connect to PostgreSQL/Redis. Error: [PASTE ERROR HERE]

Please help me:
1. Check docker-compose networking
2. Verify connection strings in .env
3. Test connectivity between containers
4. Update host configurations if needed
```

### Missing Dependencies
```
Getting ModuleNotFoundError for [MODULE NAME] in kilometers-workflow.

Please:
1. Check if it's in requirements.txt
2. Ensure virtual environment is activated
3. Install missing package
4. Update requirements.txt if needed
```

## For Running Specific Components

### Test Individual Agent
```
Help me test just the market validation agent in isolation:
1. Create a simple test script
2. Mock any external dependencies
3. Run with sample data
4. Verify output format

Location: /projects/kilometers.ai/kilometers-workflow/agents/market-validation/
```

### API Endpoint Testing
```
Help me test the workflow API endpoints:
1. Start the FastAPI server
2. Create HTTP requests to test each endpoint
3. Test WebSocket connection
4. Verify response formats

Use httpx or curl for testing.
```

### Workflow Debugging
```
The workflow starts but gets stuck at [STAGE NAME]. Help me:
1. Add debug logging to see state transitions
2. Check LangGraph state at each step
3. Verify agent outputs are correct
4. Test the failing stage in isolation
```

## Quick Fix Commands

### Reset Everything
```
Help me completely reset the kilometers-workflow project:
1. Stop all Docker containers
2. Remove volumes
3. Clean Python cache
4. Reinstall dependencies
5. Start fresh
```

### Update Dependencies
```
Update all dependencies in kilometers-workflow to latest compatible versions:
1. Backup current requirements.txt
2. Update packages safely
3. Test that everything still works
4. Update pyproject.toml
```