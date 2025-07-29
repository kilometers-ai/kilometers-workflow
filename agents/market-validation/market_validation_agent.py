"""
Market Validation Agent
Researches competitors, identifies gaps, and validates market demand
"""

import json
from typing import Any, Dict, List

from crewai import Task
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun

from ..base import AgentConfig, AgentResult, BaseAgent


class MarketValidationAgent(BaseAgent):
    """Agent responsible for market research and validation"""

    def __init__(self):
        config = AgentConfig(
            name="Market Analyst",
            role="Senior Market Research Analyst",
            goal="Analyze market opportunities and validate demand for the proposed solution",
            backstory="""You are an experienced market analyst with 15 years in tech
            market research. You excel at identifying market gaps, analyzing competitors,
            and validating product ideas. You use data-driven approaches and have a keen
            eye for emerging trends.""",
            tools=["web_search", "competitor_analysis", "market_trends"],
            temperature=0.5,  # Lower temperature for more focused analysis
        )
        super().__init__(config)

    def _get_tools(self) -> List[Tool]:
        """Market validation specific tools"""
        search = DuckDuckGoSearchRun()

        tools = [
            Tool(
                name="web_search",
                func=search.run,
                description="Search the web for market information, competitors, and trends",
            ),
            Tool(
                name="competitor_analysis",
                func=self._analyze_competitor,
                description="Analyze a specific competitor's features and market position",
            ),
            Tool(
                name="market_trends",
                func=self._analyze_market_trends,
                description="Analyze current market trends and growth potential",
            ),
        ]
        return tools

    async def execute(self, context: Dict[str, Any]) -> AgentResult:
        """Execute market validation for the given project idea"""
        try:
            project_idea = context.get("project_idea", "")

            # Create validation tasks
            tasks = [
                self.create_task(
                    f"Research existing competitors for: {project_idea}. "
                    "List top 5 competitors with their key features and pricing.",
                    context,
                ),
                self.create_task(
                    f"Identify market gaps and opportunities for: {project_idea}. "
                    "What problems are not being solved by current solutions?",
                    context,
                ),
                self.create_task(
                    f"Validate market demand for: {project_idea}. "
                    "Provide data on market size, growth rate, and target audience.",
                    context,
                ),
                self.create_task(
                    "Create a market validation report with recommendations on whether to proceed.",
                    context,
                ),
            ]

            # Execute tasks (in real implementation, would use Crew)
            results = await self._execute_tasks(tasks)

            # Compile results
            validation_report = self._compile_validation_report(results)

            return AgentResult(
                success=True,
                output=validation_report,
                artifacts=[
                    {
                        "type": "market_report",
                        "name": "market_validation_report.json",
                        "content": json.dumps(validation_report, indent=2),
                    }
                ],
            )

        except Exception as e:
            return self.handle_error(e)

    def _analyze_competitor(self, competitor_name: str) -> str:
        """Analyze a specific competitor"""
        # In production, this would use real APIs or web scraping
        return f"Analysis of {competitor_name}: Features, pricing, market share..."

    def _analyze_market_trends(self, market_segment: str) -> str:
        """Analyze market trends for a segment"""
        # In production, this would use real data sources
        return f"Market trends for {market_segment}: Growth rate, emerging technologies..."

    async def _execute_tasks(self, tasks: List[Task]) -> List[Dict[str, Any]]:
        """Execute CrewAI tasks"""
        # Placeholder for CrewAI execution
        # In production: crew = Crew(agents=[self.crew_agent], tasks=tasks)
        # results = await crew.kickoff()
        return [
            {
                "task": "competitor_research",
                "result": {
                    "competitors": [
                        {
                            "name": "Jira",
                            "features": ["Issue tracking", "Agile boards"],
                            "pricing": "$7.75/user/month",
                        },
                        {
                            "name": "Linear",
                            "features": ["Fast UI", "Keyboard shortcuts"],
                            "pricing": "$8/user/month",
                        },
                        {
                            "name": "Asana",
                            "features": ["Project management", "Timeline view"],
                            "pricing": "$10.99/user/month",
                        },
                    ]
                },
            },
            {
                "task": "market_gaps",
                "result": {
                    "gaps": [
                        "Complex setup and configuration in existing tools",
                        "Lack of AI-powered automation",
                        "Poor developer experience",
                    ]
                },
            },
            {
                "task": "market_demand",
                "result": {
                    "market_size": "$9.3B",
                    "growth_rate": "13.8% CAGR",
                    "target_audience": "Software development teams 10-500 people",
                },
            },
        ]

    def _compile_validation_report(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Compile results into a comprehensive report"""
        return {
            "market_validation": {
                "project_viability": "HIGH",
                "market_opportunity_score": 8.5,
                "competitors": results[0]["result"]["competitors"],
                "market_gaps": results[1]["result"]["gaps"],
                "market_metrics": results[2]["result"],
                "recommendation": "Proceed with development focusing on AI automation and "
                "developer experience",
                "risks": ["Highly competitive market", "Need for significant differentiation"],
                "next_steps": [
                    "Define unique value proposition",
                    "Create detailed feature roadmap",
                    "Identify early adopter segments",
                ],
            }
        }
