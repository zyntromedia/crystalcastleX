Here's the **updated, production-ready `CONTRIBUTING.md`** aligned with your new repo structure (`frontend/` • `backend/` • `development/`) and standards ✅

---

# 🤝 Contributing to CrystalCastle 🏰

> Workflow automation & governance system — maintained by **@crystalcastle-team**

---

## 🎯 Quick Start

```bash
# 1. Clone the correct repository
git clone https://github.com/zyntromedia/crystalcastleX.git
cd crystalcastleX

# 2. Install dependencies
pnpm install

# 3. Create your feature branch
git checkout -b feature/your-description-here

# 4. Start development
pnpm run dev      # Frontend → localhost:5173
pnpm run dev:backend  # Backend → separate watcher
```

---

## 📁 New Repository Structure

```
crystalcastleX/
├── frontend/          # Client-facing apps & assets
│   ├── index.html
│   ├── product.html
│   ├── style.css
│   ├── product.js
│   └── tests/         # Playwright specs
├── backend/           # Server-side logic & APIs
│   ├── index.js
│   ├── api/
│   ├── lib/
│   ├── services/
│   ├── models/
│   └── tests/
├── development/       # Docs, guides, governance
│   ├── docs/
│   │   └── knowledge/
│   ├── roadmap.md
│   └── governance.md
├── .github/
│   ├── workflows/
│   └── CODEOWNERS
├── package.json
└── playwright.config.ts
```

---

## 🧑‍💻 Development Workflow

### Branch Naming Convention
```
feature/short-desc   → New functionality
fix/issue-description → Bug fixes
chore/topic           → Maintenance, refactors, CI
docs/section          → Documentation updates
```

### Before You Push
```bash
# ✅ Always run these locally first
pnpm run lint          # Catch style issues
pnpm run test          # Run all Playwright tests
pnpm run build         # Verify frontend compiles

# ✅ Validate paths & structure
# (Auto-checked by CI — but run locally if unsure)
find . -type d -name "*.md"  # → No output = clean
```

### Commit Message Standard
```
type(scope): concise description

[optional longer explanation]

- Bullet points for details
```
**Types:** `feat` • `fix` • `chore` • `docs` • `refactor` • `test`

**Examples:**
```
fix: resolve howtotos.md file/directory conflict
feat: add user auth endpoints
chore: restructure repo → frontend/ + backend/ + development/
docs: update contributing guide
```

---

## ✅ Pull Request Process

1. **Target Branch:** `main`
2. **Title:** Follows Conventional Commits (above)
3. **Description:** Fill template — what / why / test steps
4. **Checks Must Pass:**
   - ✅ `🛡️ Validate Paths & Structure`
   - ✅ `🧪 Manual Playwright Test`
   - ✅ Lint → Build → Deploy Preview
5. **Review:** At least 1 approval required
6. **Merge:** Squash & Merge → keep history clean

---

## 📂 Where to Contribute

| Area | Folder | Team |
|---|---|---|
| Frontend UI & pages | `frontend/` | @crystalcastle-team |
| Backend API & services | `backend/` | @Develop-Team |
| Docs, guides, knowledge base | `development/docs/` | @Docs-Team |
| Workflows & automation | `.github/workflows/` | Platform Engineering |

---

## ⚠️ Critical Rules

- ❌ **Never create directories ending in `.md`** → causes Git checkout failure (`exit code 128`)
- ✅ Use `docs/topic/index.md` (folder + file) OR `topic.md` (file only) — **not both**
- ✅ All action references use **pinned SHA** (no floating `@v4`)
- ✅ Rebase your branch if `main` has diverged before merging
- ✅ No secrets/tokens committed — use repository secrets

---

## 🧩 Common Tasks

| Task | Command |
|---|---|
| Start frontend dev server | `pnpm run dev` |
| Start backend watcher | `pnpm run dev:backend` |
| Run all tests | `pnpm run test` |
| Run specific test file | `pnpm run test frontend/tests/login.spec.ts` |
| Lint & fix | `pnpm run lint:fix` |
| Build frontend | `pnpm run build` |
| Update import paths after restructure | `pnpm run migrate:paths` |

---

## 🆘 Need Help?

- **Discussions:** GitHub → Discussions tab
- **Issues:** Tag with appropriate label (`area:frontend`, `area:backend`)
- **Structure Conflicts?** → See `development/docs/knowledge/path-validation.md`
- **Maintainers:** @crystalcastle-team

---

> **CrystalCastle** — built with 💜 by [@crystalcastle](https://github.com/zyntromedia)

---

## 🚀 Ready to Use — Copy & Save As:
```
CONTRIBUTING.md
```

Then commit:
```bash
git add CONTRIBUTING.md
git commit -m "docs: rewrite contributing guide for new structure"
git push -u origin zyntromedia-patch-3
```
