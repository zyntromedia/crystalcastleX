# 📄 README.md — crystalcastleX

```markdown
# 🏰 CrystalCastle X

> **Modular AI-Powered Knowledge & Automation Platform**
> Build, orchestrate, and deploy intelligent workflows — secure, scalable, observable.

---

## 🚀 Overview

**CrystalCastle X** is a full-stack automation and AI orchestration platform designed for developers, teams, and AI practitioners. It combines **FastAPI backend**, **Docker-ready services**, **GitHub Actions CI/CD**, and **Smoke Tests** into a production-ready foundation.

---

## ✨ Key Features

- 🧠 **AI Orchestration** — Agent workflows, MCP (Model Context Protocol) integration
- ⚡ **FastAPI Backend** — High-performance async API, OpenAPI docs, type-safe
- 🐳 **Local Stack** — One-command development with Docker Compose
- ✅ **Smoke Tests** — End-to-end health checks on every deployment
- 🔐 **Security First** — Least-privilege permissions, environment-based config
- 📊 **Observability** — Status endpoints, structured logging, health monitoring
- 🧩 **Modular Skills System** — Extensible capabilities via skills directory
- 📦 **Ready to Deploy** — Docker, CI/CD, and cloud configurations included

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

> **Badge:** [![Smoke Tests](https://github.com/1napz/crystalcastleX/actions/workflows/smoke.yml/badge.svg)](https://github.com/1napz/crystalcastleX/actions/workflows/smoke.yml)

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
| `/docs` | Auto-generated API documentation |

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

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 💬 Support

- 📋 [Issues](https://github.com/1napz/crystalcastleX/issues)
- 📖 [Actions / CI Status](https://github.com/1napz/crystalcastleX/actions)
- 🏠 Repository: **github.com/1napz/crystalcastleX**

---

<p align="center">
  <i>Built with ❤️ by the crystalcastleX team</i>
</p>
```

---

✅ **README.md Ready!** Comprehensive, professional, and aligned with your Smoke Tests + FastAPI + Docker setup.

### 📋 Quick Facts Included
- ✅ Project overview & features
- ✅ One-command quick start
- ✅ Smoke Tests CI explanation + badge
- ✅ Project structure & endpoints
- ✅ Contributing guide & roadmap
- ✅ Links to issues, actions, and repo

Want me to **add shields/badges at the top**, **adjust the tech stack section**, or **save this directly to a PR**? 🚀📄
