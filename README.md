# 👾 Glitch4ce - The Retro Mini-Games Arcade

[![Live Demo](https://img.shields.io/badge/🕹️_Live_Demo-glitch4ce.onrender.com-00e5ff?style=for-the-badge&logo=render&logoColor=white)](https://glitch4ce.onrender.com)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-000000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-ff007f.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

> 🕹️ **Live Arcade Portal**: **[https://glitch4ce.onrender.com](https://glitch4ce.onrender.com)**

A production-grade, interactive retro-gaming portal built with **Flask**, **SQLAlchemy ORM**, **Flask-Login**, and styled with a vibrant, hardware-accelerated **cyberpunk synthwave aesthetic**. Players can authenticate, explore a catalog of 15+ mini-games, launch them in a seamless fullscreen container, and view real-time gameplay history tracked via robust relational models.

---

## 🎮 Key Features

- **Cyberpunk Console Interface**: Responsive dashboard featuring an interactive 3D perspective grid floor, ambient nebula glow orbs, CRT scanlines, and an interactive particle node constellation network.
- **15+ Playable Mini-Games**:
  * **Puzzle**: 2048, Crossword, Candy Crush, Quiz, Maze
  * **Arcade & Action**: Flappy Bird, Pong, Whack-a-Mole, Tower Block, Stone Paper Scissors
  * **Memory & Logic**: Memory Match, Math Sequence, Tic-Tac-Toe, Tricky, Relationship Quiz
- **Secure Authentication & Session State**: Supports passcode-protected player profiles (salted password hashing with `Werkzeug.security`), as well as instant frictionless guest access.
- **Live Real-time History Tracking**: Telemetry API (`/api/history`, `/start_game/<name>`, `/end_game/<name>`) logging gameplay sessions and durations to SQLAlchemy ORM with UTC timestamps.
- **Admin Management Console**: Dedicated `/admin` dashboard with CSRF-protected player management and telemetry aggregations.
- **Full CI/CD & Automated Testing**: Automated test suite (`pytest`) covering unit models, authentication flows, route protections, and JSON APIs with GitHub Actions CI pipeline.

---

## 🛠️ Technology Stack

* **Backend**: Python 3.11+, Flask (Application Factory Pattern)
* **ORM & Database**: Flask-SQLAlchemy 3.1+, SQLite / PostgreSQL compatible
* **Authentication & Security**: Flask-Login, Flask-WTF (CSRF), Flask-Limiter (Rate Limiting), Werkzeug Password Hashing
* **Frontend**: HTML5, Vanilla CSS3 (Perspective transforms, flexbox grid, glassmorphism), JavaScript (HTML5 Canvas physics, Fetch API)
* **Testing & Quality**: Pytest, Ruff Linter, GitHub Actions CI
* **WSGI Deployment**: Gunicorn, Render / Heroku ready

---

## 📂 Project Architecture

```text
Glitch4ce/
├── .gitattributes           # GitHub Linguist language override
├── docs/
│   └── API.md               # Complete REST API specification
├── app/
│   ├── __init__.py          # Application Factory & Security Middleware
│   ├── config.py            # Environment-aware Config (Dev, Test, Prod)
│   ├── extensions.py        # Extensions: db, login_manager, csrf, limiter, migrate
│   ├── models.py            # SQLAlchemy models (User, GameplaySession, GameScore)
│   ├── forms.py             # Secure WTForms for login & registration
│   ├── routes/
│   │   ├── auth.py          # /login, /register, /logout
│   │   ├── main.py          # /, /games, /profile, telemetry & leaderboard APIs
│   │   ├── games.py         # Dynamic routes & endpoint registry for 15+ games
│   │   ├── admin.py         # /admin player and telemetry dashboard
│   │   └── errors.py        # 400, 401, 403, 404, 429, 500 cyberpunk error handlers
│   └── utils/
│       ├── migrate_data.py  # SQLite to SQLAlchemy database migration utility
│       └── seed_data.py     # Database mock data seeder utility
├── templates/               # Cyberpunk Jinja2 templates
│   ├── admin/               # Admin portal views
│   ├── errors/              # Custom error pages
│   ├── profile.html         # Player profile overview
│   └── Games/               # Arcade Hub and mini-game templates
├── static/                  # Static assets (images, game audio, stylesheets)
│   ├── css/cyberpunk.css    # Synthwave CRT scanlines & neon animations
│   └── js/game_launcher.js  # Telemetry & fullscreen launcher module
├── tests/                   # Automated test suite (pytest - 26 tests)
│   ├── conftest.py          # Pytest application & database fixtures
│   ├── test_models.py       # Model & password hashing unit tests
│   ├── test_auth.py         # Authentication integration tests
│   ├── test_routes.py       # Route & template integration tests
│   └── test_api.py          # Telemetry & score API integration tests
├── .github/workflows/
│   └── ci.yml               # GitHub Actions CI workflow (python matrix + pytest)
├── app.py                   # WSGI Application Entrypoint
├── show_database.py         # CLI database telemetry inspector
├── requirements.txt         # Pinned production dependencies
└── .env.example             # Environment variable template
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+ installed on your system.
* pip package manager.

### Local Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Spidey173/Glitch4ce.git
   cd Glitch4ce
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   ```bash
   cp .env.example .env
   ```

5. **Start the Application**:
   ```bash
   python app.py
   ```

6. **Launch in Browser**:
   Open [http://localhost:5000](http://localhost:5000) to enter the portal.

---

## 🧪 Testing & Code Quality

Run the automated test suite with **pytest**:
```bash
pytest -v
```

Run static analysis and linting with **ruff**:
```bash
ruff check .
```

Seed database with mock telemetry data:
```bash
python app/utils/seed_data.py
```

Inspect database records from terminal:
```bash
python show_database.py
```

---

## 🎯 API & Route Map

| Endpoint | Method | Function |
|---|---|---|
| `/` | GET | Session validation & redirector |
| `/login` | GET, POST | Player authentication & guest access |
| `/register` | GET, POST | Register protected player account |
| `/logout` | GET | Clears active player sessions |
| `/games` | GET | Main Arcade Hub dashboard |
| `/profile` | GET | Player metrics, badges, and high score history |
| `/admin` | GET | Admin telemetry & player manager |
| `/admin/player/<username>/delete` | POST | CSRF-protected player removal |
| `/start_game/<game_name>` | POST | Logs game start & session ID |
| `/end_game/<game_name>` | POST | Records session completion & duration |
| `/api/history` | GET | Real-time player history JSON |
| `/api/score/submit` | POST | Submits mini-game high score |
| `/api/leaderboard/<game_name>` | GET | Retrieves top 10 scores per game |
| `/api/health` | GET | Telemetry & system health check |


---

## 👤 Developer Profile

* **Developer**: Pruthvi R
* **Github**: [@Spidey173](https://github.com/Spidey173)
* **LinkedIn**: [Pruthvi R](https://www.linkedin.com/in/pruthvi-r-48ba9b2b4/)

---

## 📝 License

This project is open-source and free to adapt under the MIT License. Have fun playing! 🕹️✨
