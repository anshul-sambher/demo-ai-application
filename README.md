# Gen Z Investment Advisory Demo

This repository provides a command-line application that delivers a gamified
investment advisory experience tailored to Gen Z investors. The app combines
habit-building quests, XP tracking, and timely market research sourced from the
Wall Street Journal (via RSS) and other credible outlets.

## Features

- 🎯 **Gamification layer** – daily quests, XP, levels, and badges to reward
  consistent financial habits.
- 📰 **Live market headlines** – pulls the latest articles from WSJ, Reuters,
  and CNBC RSS feeds with a fallback dataset when offline.
- 📈 **Trending asset radar** – highlights popular tickers using Yahoo Finance's
  public trending endpoint.
- 🧭 **Risk-aware guidance** – generates playbooks for starter, confident, and
  adventurer-style investors.

## Getting Started

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the advisor:

   ```bash
   python main.py --username "Avery" --risk-profile Adventurer
   ```

   Use `--limit` to control the number of headlines pulled per source.

## How It Works

- `investment_app/data_sources.py` fetches RSS feeds from WSJ and peers. If the
  network is unavailable, it returns a curated offline dataset.
- `investment_app/gamification.py` defines quests, badges, and XP progression to
  keep the experience engaging for younger investors.
- `investment_app/advisor.py` translates live data and player progress into a
  set of actionable insights and recommendations.
- `investment_app/app.py` stitches everything together into a CLI-friendly
  report.

## Extending the Demo

- Hook into premium data sources or broker APIs for personalized positions.
- Persist user progress and streaks with a lightweight database.
- Convert the CLI into a web or mobile experience to add social leaderboards.

## Disclaimer

This project is for demonstration purposes only and does not constitute
financial advice. Always conduct your own research or consult a licensed
professional before making investment decisions.
