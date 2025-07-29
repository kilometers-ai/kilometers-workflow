"""
Base Agent class for all SDLC agents
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from crewai import Agent, Task
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    """Configuration for an agent"""

    name: str
    role: str
    goal: str
    backstory: str
    tools: List[str] = Field(default_factory=list)
    llm_model: str = "gpt-4"
    temperature: float = 0.7
    max_iterations: int = 5


class AgentResult(BaseModel):
    """Result from an agent execution"""

    success: bool
    output: Dict[str, Any]
    artifacts: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    requires_escalation: bool = False
    escalation_reason: Optional[str] = None


class BaseAgent(ABC):
    """Abstract base class for all SDLC agents"""

    def __init__(self, config: AgentConfig):
        self.config = config
        self.llm = ChatOpenAI(model=config.llm_model, temperature=config.temperature)
        self.crew_agent = self._create_crew_agent()

    def _create_crew_agent(self) -> Agent:
        """Create the CrewAI agent instance"""
        return Agent(
            role=self.config.role,
            goal=self.config.goal,
            backstory=self.config.backstory,
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=self.config.max_iterations,
            tools=self._get_tools(),
        )

    @abstractmethod
    def _get_tools(self) -> List[Any]:
        """Get the tools available to this agent"""
        pass

    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Execute the agent's main task"""
        pass

    def create_task(self, description: str, context: Dict[str, Any]) -> Task:
        """Create a CrewAI task for this agent"""
        return Task(description=description, agent=self.crew_agent, context=context)

    def handle_error(self, error: Exception) -> AgentResult:
        """Standard error handling for agents"""
        return AgentResult(
            success=False,
            output={},
            errors=[str(error)],
            requires_escalation=self._should_escalate(error),
        )

    def _should_escalate(self, error: Exception) -> bool:
        """Determine if an error requires escalation"""
        # Override in subclasses for specific escalation logic
        return "complex" in str(error).lower() or "unclear" in str(error).lower()
