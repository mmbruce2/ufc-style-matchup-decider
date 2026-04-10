# UFC Style Matchup Decider

A compact UFC decision tool that compares fighter style profiles using public UFC stats.

It builds a simple matchup framework around four ideas:

- striking edge
- wrestling pressure
- defensive control
- submission threat

Then it visualizes the style map and outputs sample matchup leans.

## What it does

- uses public UFC-style fighter metrics
- builds a control score and grappling score for each fighter
- creates a style map of striking edge vs grappling score
- creates a fighter ranking chart by control score
- compares sample matchup pairs and outputs a simple lean

## How to run

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Output files

- `outputs/fighter_control_scores.png`
- `outputs/style_matchup_map.png`
- `outputs/sample_matchup_edges.csv`

## What the output shows

### Fighter control score chart
Ranks the fighters by a blend of strike differential and takedown defense.

### Style matchup map
Plots striking edge against grappling score so you can quickly see archetypes:
- striker-heavy profiles
- grappler-heavy profiles
- balanced contenders

### Sample matchup table
Compares three sample fights and shows:
- striking edge
- wrestling edge
- defensive edge
- submission edge
- total edge
- model lean

## Data source

- UFC fighter statistics from public UFC Stats style metrics: <http://ufcstats.com/statistics/fighters>

## Why this is useful

This is a narrow portfolio project with:

- a sports decision angle
- visualizations
- structured decision output
- simple explainability

It answers a useful question: **which fighter style profile should have the edge before you even get into narrative hype?**
