# 🇮🇳 Website Update Agent

Production-ready monitoring agent for Indian government, education, scholarship, university and examination websites.

## Included
- FastAPI REST API + JWT admin authentication
- SQLite by default; PostgreSQL-ready through DATABASE_URL
- Generic HTML and RSS monitoring with configurable selectors
- SHA-256 fingerprints and duplicate suppression
- Categories, importance and keyword matching
- Per-site intervals through APScheduler
- Telegram + SMTP notifications
- Responsive dashboard with manual scans
- Docker Compose and GitHub Actions CI
- Seed list for LNMU, BSEB, Bihar Raj Bhavan, MedhaSoft, Bihar PMS, NSP, Sarkari Result, BPSC, UPSC and SSC

## Run
1. Copy `.env.example` to `.env` and set a strong `SECRET_KEY` and `ADMIN_PASSWORD`.
2. `pip install -r backend/requirements.txt`
3. `python backend/seed.py`
4. `uvicorn backend.app.main:app --reload`
5. Open `/docs` for API docs.

## Docker
`cp .env.example .env && docker compose up -d --build`

## Production hardening
Use PostgreSQL, HTTPS, a reverse proxy, restricted CORS, strong secrets, outbound URL allowlisting/SSRF controls, rate limiting, and a process supervisor. Respect robots.txt, terms, site rate limits and applicable law. The monitor never fabricates missing dates or facts.

## Extending
Add websites from `POST /api/websites` without source changes. `monitor_type` supports `html` and `rss`; Playwright/PDF adapters can be added independently.

Seeded URLs are official/source sites where available. Sarkari Result is a third-party informational source and should not replace the official government source.
