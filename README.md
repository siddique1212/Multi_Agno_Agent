
# Multi-Agent Task Force: Mission Sustainability

This is a reference implementation for the lab **"Multi-Agent Task Force: Mission Sustainability"**.
It provides four agents (News Analyst, Data Analyst, Policy Reviewer, Innovations Scout) and a Streamlit UI to run them individually or as a team and to combine outputs into a single proposal.

## Features
- **News Analyst**: mock search for recent city-level sustainability initiatives.
- **Policy Reviewer**: mock search for policy updates in a target city.
- **Innovations Scout**: mock search for emerging green-tech ideas.
- **Data Analyst**: analyzes an air-quality CSV (or uses a demo dataset) and summarizes trends.
- **Team Mode**: orchestrates all agents and generates a combined proposal.

> Note: Search tools are offline mocks so the app runs without external keys. You can replace them with real APIs later.

## Quickstart
1. Create a virtual environment (recommended) and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. (Optional) Prepare your CSV with columns: `date, pm25, pm10, no2, city`.

## Customization
- Replace the mocks in `agents.py` (`GoogleSearchTools`, `HackerNewsTools`) with real search APIs.
- Extend `TeamOrchestrator.run_team` to parallelize execution if desired.

## Folder structure
```
Multi_Agno_Gent/
├── app.py
├── agents.py
├── tools.py
├── requirements.txt
├── README.md
└── sample_data.csv
```
