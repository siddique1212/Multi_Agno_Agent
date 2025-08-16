
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import pandas as pd
import io
import statistics
from datetime import datetime

@dataclass
class AgentResult:
    title: str
    summary: str
    artifacts: Dict[str, Any] = field(default_factory=dict)

class BaseAgent:
    name: str = "BaseAgent"
    role: str = "Generic"

    def run(self, **kwargs) -> AgentResult:
        raise NotImplementedError

# --- Tools (Mock) ---
class GoogleSearchTools:
    """A tiny offline mock to emulate search results. Replace with real search API if available."""
    @staticmethod
    def search(query: str, limit: int = 5) -> List[Dict[str, str]]:
        canned = [
            {"title": "Karachi launches coastal mangrove restoration plan",
             "link": "https://example.org/news/mangrove-restoration",
             "snippet": "City partners with NGOs to plant 1 million mangroves to boost blue carbon."},
            {"title": "Lahore pilots electric buses for BRT corridors",
             "link": "https://example.org/news/e-bus-lahore",
             "snippet": "50 e-buses reduce PM2.5 hotspots and operating costs by 20%."},
            {"title": "Islamabad installs smart air-quality monitors",
             "link": "https://example.org/news/smart-aqis",
             "snippet": "Open data platform to inform traffic restrictions on smog days."},
            {"title": "Karachi rooftop solar incentive expands",
             "link": "https://example.org/news/rooftop-solar",
             "snippet": "Net metering and low-interest loans for households and SMEs."},
            {"title": "Peshawar launches plastic-free markets initiative",
             "link": "https://example.org/news/plastic-free",
             "snippet": "Alternatives and vendor training in 5 pilot bazaars."},
        ]
        # Simple filter by keywords in query
        q = query.lower()
        filtered = [r for r in canned if any(tok in r["title"].lower() or tok in r["snippet"].lower() for tok in q.split())]
        return (filtered or canned)[:limit]

class HackerNewsTools:
    @staticmethod
    def search(query: str, limit: int = 5) -> List[Dict[str, str]]:
        ideas = [
            {"title": "Lithium-free sodium-ion streetlight batteries", "link": "https://example.org/hn/sodium-ion"},
            {"title": "Modular microforests for ultra-dense cities", "link": "https://example.org/hn/microforests"},
            {"title": "AI-driven dynamic bus headways cut idle time", "link": "https://example.org/hn/ai-bus"},
            {"title": "Permeable solar pavement tiles for sidewalks", "link": "https://example.org/hn/solar-tiles"},
            {"title": "District cooling via treated wastewater", "link": "https://example.org/hn/district-cooling"},
        ]
        q = query.lower()
        filtered = [r for r in ideas if any(tok in r["title"].lower() for tok in q.split())]
        return (filtered or ideas)[:limit]

# --- Agents ---
class NewsAnalystAgent(BaseAgent):
    name = "News Analyst"
    role = "Find recent sustainability initiatives"

    def run(self, topic: str = "city-level green projects", limit: int = 5, **kwargs) -> AgentResult:
        results = GoogleSearchTools.search(topic, limit=limit)
        lines = [f"- [{r['title']}]({r['link']}): {r['snippet']}" for r in results]
        summary = "Recent items related to sustainability initiatives:\n" + "\n".join(lines)
        return AgentResult(title="News Digest", summary=summary, artifacts={"results": results})

class PolicyReviewerAgent(BaseAgent):
    name = "Policy Reviewer"
    role = "Summarize government policy updates"

    def run(self, city: str = "Karachi", limit: int = 5, **kwargs) -> AgentResult:
        query = f"{city} sustainability policy update"
        results = GoogleSearchTools.search(query, limit=limit)
        bullet_points = [f"- {r['title']}: {r['snippet']}" for r in results]
        summary = f"Policy signals for {city}:\n" + "\n".join(bullet_points)
        return AgentResult(title=f"Policy Brief: {city}", summary=summary, artifacts={"results": results})

class InnovationsScoutAgent(BaseAgent):
    name = "Innovations Scout"
    role = "Find innovative green tech ideas"

    def run(self, query: str = "urban sustainability tech", limit: int = 5, **kwargs) -> AgentResult:
        results = HackerNewsTools.search(query, limit=limit)
        lines = [f"- [{r['title']}]({r['link']})" for r in results]
        summary = "Promising innovations:\n" + "\n".join(lines)
        return AgentResult(title="Innovation Radar", summary=summary, artifacts={"results": results})

class DataAnalystAgent(BaseAgent):
    name = "Data Analyst"
    role = "Analyze environmental datasets"

    def run(self, csv_bytes: Optional[bytes] = None, city: str = "Karachi", **kwargs) -> AgentResult:
        """
        Accepts CSV bytes with columns like: date,pm25,pm10,no2,city
        If none provided, returns guidance and example stats for a demo dataset.
        """
        if csv_bytes:
            df = pd.read_csv(io.BytesIO(csv_bytes), parse_dates=["date"])
        else:
            df = pd.DataFrame({
                "date": pd.date_range("2025-01-01", periods=30, freq="D"),
                "pm25": [50,48,45,52,60,55,58,62,49,47,46,45,44,50,52,51,48,46,45,43,42,40,39,41,44,46,49,47,45,43],
                "pm10": [90,88,85,92,100,95,98,102,89,87,86,85,84,90,92,91,88,86,85,83,82,80,79,81,84,86,89,87,85,83],
                "no2": [30,32,31,29,35,34,33,36,31,30,29,28,27,31,32,33,30,29,28,27,26,25,24,25,26,27,28,27,26,25],
                "city": [city]*30
            })
        # Compute simple trends
        df = df.sort_values("date")
        stats = {
            "n_days": len(df),
            "pm25_avg": round(float(df["pm25"].mean()), 2) if "pm25" in df else None,
            "pm25_median": round(float(df["pm25"].median()), 2) if "pm25" in df else None,
            "pm25_latest": float(df["pm25"].iloc[-1]) if "pm25" in df else None,
            "pm25_change_7d": None,
        }
        if "pm25" in df and len(df) >= 8:
            stats["pm25_change_7d"] = round(float(df["pm25"].iloc[-1] - df["pm25"].iloc[-8]), 2)
        trend = "decreasing" if stats["pm25_change_7d"] is not None and stats["pm25_change_7d"] < 0 else "increasing or stable"
        summary = (
            f"Analyzed {stats['n_days']} days for {df['city'].iloc[0]}.\n"
            f"- PM2.5 average: {stats['pm25_avg']}\n"
            f"- PM2.5 median: {stats['pm25_median']}\n"
            f"- Latest PM2.5: {stats['pm25_latest']}\n"
            f"- 7-day change: {stats['pm25_change_7d']} ({trend})"
        )
        return AgentResult(title="Air Quality Summary", summary=summary, artifacts={"dataframe": df, "stats": stats})

# --- Team Orchestrator ---
class TeamOrchestrator:
    def __init__(self):
        self.news = NewsAnalystAgent()
        self.data = DataAnalystAgent()
        self.policy = PolicyReviewerAgent()
        self.innov = InnovationsScoutAgent()

    def run_single(self, agent_name: str, **kwargs) -> AgentResult:
        agent_map = {
            "News Analyst": self.news,
            "Data Analyst": self.data,
            "Policy Reviewer": self.policy,
            "Innovations Scout": self.innov,
        }
        agent = agent_map.get(agent_name)
        if not agent:
            raise ValueError(f"Unknown agent: {agent_name}")
        return agent.run(**kwargs)

    def run_team(self, inputs: Dict[str, Any]) -> AgentResult:
        # Run agents (sequential for reproducibility)
        news_res = self.news.run(topic=inputs.get("news_topic", "city-level green projects"), limit=5)
        data_res = self.data.run(csv_bytes=inputs.get("csv_bytes"), city=inputs.get("city", "Karachi"))
        policy_res = self.policy.run(city=inputs.get("city", "Karachi"), limit=5)
        innov_res = self.innov.run(query=inputs.get("innov_query", "urban sustainability tech"), limit=5)

        # Combine into a high-level proposal
        proposal = f"""# Sustainability Proposal for {inputs.get('city','Your City')}

## Executive Summary
This proposal synthesizes signals from recent news, policy updates, environmental data, and emerging innovations to suggest actionable steps for urban sustainability.

## 1) News Insights
{news_res.summary}

## 2) Policy Landscape
{policy_res.summary}

## 3) Environmental Data Highlights
{data_res.summary}

## 4) Innovation Opportunities
{innov_res.summary}

## 5) Recommended Actions (Draft)
- Scale rooftop solar with net metering and low-interest financing.
- Pilot e-buses on the highest pollution corridors informed by AQ data.
- Expand mangrove/coastal restoration to enhance blue carbon and flood resilience.
- Open AQ data and set smog-day response protocols.
- Explore sodium-ion batteries and solar pavement pilots in busy districts.
"""
        return AgentResult(
            title="Combined Sustainability Proposal",
            summary=proposal,
            artifacts={
                "news": news_res.artifacts,
                "data": data_res.artifacts,
                "policy": policy_res.artifacts,
                "innovation": innov_res.artifacts,
            }
        )
