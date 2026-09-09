# 📄 Updated README.md — With Badges & Tech Stack

```markdown
# 🏰 CrystalCastle X

> **Modular AI-Powered Knowledge & Automation Platform**
> Build, orchestrate, and deploy intelligent workflows — secure, scalable, observable.

---

## 🛡️ Status & Badges

[![Smoke Tests](https://github.com/1napz/crystalcastleX/actions/workflows/smoke.yml/badge.svg)](https://github.com/1napz/crystalcastleX/actions/workflows/smoke.yml)
[![GitHub Release](https://img.shields.io/github/v/release/1napz/crystalcastleX?style=flat-square)](https://github.com/1napz/crystalcastleX/releases)
[![License](https://img.shields.io/github/license/1napz/crystalcastleX?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Code Style](https://img.shields.io/badge/Code%20Style-PyTest-009EDC?style=flat-square&logo=pytest&logoColor=white)](https://docs.pytest.org/)

---

## 🚀 Overview

**CrystalCastle X** is a full-stack automation and AI orchestration platform designed for developers, teams, and AI practitioners. It combines a high-performance **FastAPI backend**, **Docker-ready services**, **GitHub Actions CI/CD**, and **end-to-end Smoke Tests** into a production-ready foundation.

---

## 🧰 Tech Stack

### 🔙 Backend & API
| Technology | Role |
|---|---|
| **Python 3.11+** | Runtime & primary language |
| **FastAPI** | High-performance async API framework • OpenAPI docs • type-safe |
| **Pydantic** | Data validation • settings • type enforcement |
| **Uvicorn** | ASGI production server |

### 🐳 Dev & Deployment
| Technology | Role |
|---|---|
| **Docker Compose** | Local development stack • one-command startup |
| **GitHub Actions** | CI/CD • Smoke Tests • automation |
| **Pytest** | Testing framework • smoke & integration tests |

### 🤖 AI & Extensibility
| Technology | Role |
|---|---|
| **MCP (Model Context Protocol)** | AI tool integration • capability expansion |
| **Modular Skills System** | Extensible features under `skills/` |

### 🔐 Security & Observability
| Technology | Role |
|---|---|
| **Environment-based config** | Secrets & configuration • no hardcoding |
| **Status Endpoints** | Health checks • `/v1/status` |
| **Least-privilege CI** | Explicit permissions • secure workflows |

---

## ✨ Key Features

- 🧠 **AI Orchestration** — Agent workflows, MCP integration
- ⚡ **FastAPI Backend** — Async, auto-docs, high-performance
- 🐳 **Local Stack** — Docker Compose, zero-config development
- ✅ **Smoke Tests** — End-to-end health checks on every PR & push
- 🔐 **Security First** — Least-privilege permissions, env-based config
- 📊 **Observability** — Health endpoints, structured logging
- 🧩 **Modular Skills** — Extensible capabilities, plugin-ready
- 📦 **Production-Ready** — Containerized, CI-tested, documented

---

## 📁 Project Structure

```
crystalcastleX/
├── .github/
│   └── workflows/
│       └── smoke.yml           # ✅ Smoke Tests CI
├── app/                         # FastAPI Application
│   ├── main.py                  # API Entry Point
│   └── [modules]
├── tests/
│   └── test_smoke_generation.py # Smoke Test Suite
├── docker-compose.yml           # Local Development Stack
├── requirements.txt             # Dependencies
├── requirements-dev.txt         # Dev Dependencies
└── README.md                    # This File
```

---

## 🛠️ Quick Start

### Prerequisites
- **Python 3.11+**
- **Docker & Docker Compose**
- **Git**

### 1️⃣ Clone & Install
```bash
git clone https://github.com/1napz/crystalcastleX.git
cd crystalcastleX
```

### 2️⃣ Start Development Stack
```bash
docker compose build
docker compose up -d
```

### 3️⃣ Verify Service
```bash
curl http://localhost:8000/v1/status
```

### 4️⃣ Run Smoke Tests
```bash
pip install -r requirements-dev.txt
pytest -q tests/test_smoke_generation.py -v
```

---

## 🧪 CI/CD — Smoke Tests

Every push to `main` and every Pull Request automatically runs:
1. 📥 Checkout code
2. 🐍 Set up Python 3.11
3. 📦 Cache dependencies
4. 🐳 Build & start Docker stack
5. ✅ Wait for service health (`/v1/status`)
6. 🧪 Run smoke tests
7. 🧹 Tear down stack

> ✅ Badge at top shows real-time status — green = passing.

---

## 🔧 Configuration

### Environment Variables
```env
API_BASE=http://localhost:8000
X_API_KEY=local-dev-key
```

### API Endpoints
| Endpoint | Description |
|---|---|
| `/v1/status` | Service health check |
| `/docs` | Auto-generated API documentation (Swagger UI) |
| `/redoc` | Alternative API documentation |

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push: `git push -u origin feature/amazing-feature`
5. Open Pull Request

> ✅ All PRs automatically run Smoke Tests — ensure they pass before merge.

---

## 📋 Roadmap

- [ ] 🧠 MCP Server integration
- [ ] 🤖 AI Agent workflow templates
- [ ] 📊 Enhanced dashboard & metrics
- [ ] 🔐 OAuth2 / JWT Authentication
- [ ] ☁️ Production deployment guides
- [ ] 📈 Code coverage reporting

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 💬 Support

- 📋 [Report Issues](https://github.com/1napz/crystalcastleX/issues)
- 📖 [CI Status & Workflows](https://github.com/1napz/crystalcastleX/actions)
- 🏠 Repository: **github.com/1napz/crystalcastleX**

---

<p align="center">
  <i>Built with ❤️ by the crystalcastleX team</i>
</p>
```

---

## ✅ What's New
- 🛡️ **7 Badges at top:** Tests • Release • License • Python • FastAPI • Docker • Code Style
- 🧰 **Tech Stack expanded:** 4 categorized tables (Backend • Dev/Deploy • AI/Extensibility • Security/Observability)
- 📋 Endpoints table + Roadmap + Quick Start all refined
- 🎨 Clean, professional, scannable layout

> 💡 **Note:** Release/badge numbers will populate automatically once you create a GitHub Release.

Want me to **open a PR with this README directly**, or adjust any section further? 🚀📄
