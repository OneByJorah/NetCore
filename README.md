<div align="center">

![nethermind banner](docs/assets/banner.svg)

# nethermind

**AI-powered network switch management** — multi-vendor SSH and serial access, 50+ Jinja2 templates, an AI agent, and security auditing for mixed network fleets.

<a href="https://github.com/OneByJorah/nethermind/stargazers"><img src="https://img.shields.io/github/stars/OneByJorah/nethermind?style=flat-square" alt="Stars"></a>
<a href="https://github.com/OneByJorah/nethermind/commits"><img src="https://img.shields.io/github/last-commit/OneByJorah/nethermind?style=flat-square" alt="Last commit"></a>
<img src="https://img.shields.io/github/license/OneByJorah/nethermind?style=flat-square" alt="License">
<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/Electron-desktop-47848F?style=flat-square&logo=electron&logoColor=white" alt="Electron desktop">

![nethermind screenshot](docs/assets/screenshot.png)

</div>

## Quick Start

```bash
git clone https://github.com/OneByJorah/nethermind.git
cd nethermind
cp .env.example .env   # set OPENAI_API_KEY and SSH credentials
docker compose up -d
```

Open **http://localhost:3000** for the web UI, or **http://localhost:8000/docs** for the API docs.

## What This Is

nethermind is a full-stack platform for managing network switches and routers across vendors. It connects over SSH or a serial console, generates configs from templates, parses existing running-configs into structured data, runs AI-assisted operations, and enforces change discipline through an approval workflow. It is built for network engineers and MSPs who manage heterogeneous hardware and want an audit trail behind every change.

> [!NOTE]
> This project has been consolidated into **hermes-switch-manager**, which is now the actively developed repository. nethermind retains its desktop application and standalone CLI.

## Features

- **Multi-vendor support** — Cisco IOS/XR/NX-OS, HP ArubaOS-Switch (ProCurve), Juniper JunOS, Arista EOS, and Linux.
- **SSH and serial console** — Netmiko for SSH, pyserial for RS-232/USB out-of-band access, plus Telnet deploy.
- **50+ Jinja2 templates** — built-in configuration templates for Aruba, Cisco, and generic devices.
- **Config parser** — turn existing running-config text into structured data for editing and re-rendering.
- **AI chat assistant** — OpenAI-powered agent with tool calling for natural-language operations.
- **IRIS-style workflow engine** — disciplined config change management with approval gates.
- **Security auditing** — CVE scanning, AAA checks, and CIS/NIST compliance findings.
- **Config diff and rollback** — compare versions and restore previous configs.
- **Device health monitoring** — CPU, memory, and interface status metrics.
- **Immutable audit trail** — every action logged with actor, target, and timestamp.
- **Desktop app** — an Electron package bundles backend and frontend into one installer.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                   Frontend                       │
│          Next.js + TypeScript + Tailwind         │
│   Dashboard │ Switches │ Configs │ Templates     │
│   Chat │ Workflows │ Security │ Topology         │
└──────────────────────┬──────────────────────────┘
                       │ REST API
┌──────────────────────▼──────────────────────────┐
│                    Backend                       │
│              FastAPI + SQLAlchemy                 │
│                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────┐ │
│  │ Netmiko SSH │  │ Serial/COM   │  │ AI     │ │
│  │ Client      │  │ Client       │  │ Agent  │ │
│  └─────────────┘  └──────────────┘  └────────┘ │
│  ┌─────────────┐  ┌──────────────┐  ┌────────┐ │
│  │ Template    │  │ Config       │  │Workflow│ │
│  │ Engine      │  │ Parser       │  │ Engine │ │
│  └─────────────┘  └──────────────┘  └────────┘ │
│  ┌─────────────┐  ┌──────────────┐  ┌────────┐ │
│  │ Deployer    │  │ Security     │  │Audit   │ │
│  │             │  │ Auditor      │  │Trail   │ │
│  └─────────────┘  └──────────────┘  └────────┘ │
└──────────────────────┬──────────────────────────┘
                       │
              ┌────────▼────────┐
              │   SQLite / PG   │
              │   Database      │
              └─────────────────┘
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/switches/` | List all switches |
| `POST` | `/api/switches/` | Add a new switch |
| `POST` | `/api/switches/{id}/backup` | Pull running config via SSH |
| `GET` | `/api/configs/{id}` | Get a config backup |
| `POST` | `/api/config/parse` | Upload `.txt` config → structured JSON |
| `POST` | `/api/config/validate` | Validate a config before deploy |
| `POST` | `/api/config/render` | Render config to CLI text |
| `POST` | `/api/config/deploy` | Deploy config to a switch |
| `GET` | `/api/templates/` | List config templates |
| `POST` | `/api/templates/render` | Render a template with variables |
| `POST` | `/api/chat/` | Chat with the AI assistant |
| `GET` | `/api/workflows/` | List workflows |
| `GET` | `/api/security/` | Security findings |
| `GET` | `/api/system/serial-ports` | List serial ports |
| `GET` | `/health` | Health check |

## Configuration

Copy `.env.example` to `.env` and set real values:

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./switches.db` | Database connection string |
| `OPENAI_API_KEY` | *(empty)* | OpenAI API key for the AI agent |
| `OPENAI_MODEL` | `gpt-4o` | Model used by the AI agent |
| `SSH_USERNAME` | `admin` | Default SSH username for switches |
| `SSH_PASSWORD` | *(empty)* | Default SSH password |
| `SECRET_KEY` | `change-me` | Application secret key |
| `LOG_LEVEL` | `INFO` | Log verbosity |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:5173` | Allowed frontend origins |
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Frontend → backend API base URL |

> [!WARNING]
> SSH passwords are stored encrypted at rest, but the default `SECRET_KEY` and SQLite database are development defaults. Set a strong `SECRET_KEY`, uncomment the PostgreSQL service, and switch `DATABASE_URL` before production use.

## CLI

nethermind also ships a CLI for quick config operations:

```bash
cd scripts
python cli.py render --hostname MY-SW --mgmt-ip 192.168.1.10
python cli.py parse /path/to/running-config.txt
python cli.py deploy --transport telnet --host 192.168.1.1 --port 9023
```

## Local Development

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Desktop App

An Electron package bundles the backend and frontend into a single app. Build with `desktop/build-win.bat` (Windows) or `desktop/build-linux.sh` (AppImage/deb/rpm), or run from source with `npx electron .` from `desktop/`.

## Use Cases

1. **Network engineers** — manage and back up a mixed-vendor fleet from one UI.
2. **MSPs** — standardize config generation and keep an audit trail per customer.
3. **Lab engineers** — pair with containerlab topologies for testing.
4. **Security teams** — run repeatable CVE/AAA/compliance audits.

## Tech Stack

FastAPI, SQLAlchemy, Netmiko, pyserial, Jinja2, OpenAI SDK, Next.js 16 (TypeScript), Tailwind CSS, Electron, SQLite/PostgreSQL, Docker Compose, uv/Ruff/pytest.

## Screenshots

| View | Preview |
|------|---------|
| Dashboard | ![Dashboard](docs/assets/screenshots/01-dashboard.png) |
| Switches | ![Switches](docs/assets/screenshots/02-switches.png) |
| Configs | ![Configs](docs/assets/screenshots/03-configs.png) |
| Templates | ![Templates](docs/assets/screenshots/04-templates.png) |
| AI chat | ![AI chat](docs/assets/screenshots/05-chat.png) |
| Workflows | ![Workflows](docs/assets/screenshots/06-workflows.png) |
| Security | ![Security](docs/assets/screenshots/07-security.png) |
| Topology | ![Topology](docs/assets/screenshots/08-topology.png) |
| Metrics | ![Metrics](docs/assets/screenshots/09-metrics.png) |
| API docs | ![API docs](docs/assets/screenshots/10-api-docs.png) |

## Project Structure

```
nethermind/
├── backend/                 # FastAPI app (routers, services, models)
├── frontend/                # Next.js dashboard
├── desktop/                 # Electron desktop packaging
├── scripts/                 # cli.py + helper scripts
├── templates/               # Config templates
├── docker-compose.yml       # Backend + frontend deployment
├── manifest.json            # Repo metadata
├── pyproject.toml           # Ruff + pytest config
├── install.sh / install.ps1
└── docs/                    # Architecture + assets
```

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), then [open an issue](https://github.com/OneByJorah/nethermind/issues) or a pull request.

## License

MIT — see [LICENSE](LICENSE).

## Connect

- [jorahone.com](https://jorahone.com)
- [GitHub Org](https://github.com/OneByJorah)
- [info@jorahone.com](mailto:info@jorahone.com)
