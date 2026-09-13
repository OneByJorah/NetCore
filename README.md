<div align="center">

![nethermind banner](docs/assets/banner.svg)

# nethermind

**AI-powered network switch management** — multi-vendor SSH and serial access, 50+ Jinja2 templates, an AI agent, and security auditing for mixed network fleets.

[![GitHub release](https://img.shields.io/github/v/release/OneByJorah/NetCore?color=009688&label=release&logo=github)](https://github.com/OneByJorah/NetCore/releases)
[![PyPI version](https://img.shields.io/pypi/v/nethermind?color=009688&label=pip&logo=pypi)](https://pypi.org/project/nethermind/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=next.js&logoColor=white)](https://nextjs.org/)
[![Electron](https://img.shields.io/badge/Electron-47848F?style=flat-square&logo=electron&logoColor=white)](https://www.electronjs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?color=FFB300&logo=open-source-initiative&logoColor=FFB300)](https://opensource.org/licenses/MIT)

</div>

![nethermind screenshot](docs/assets/screenshot.png)

## What This Is

nethermind is a full-stack platform for managing network switches and routers across vendors. It connects over SSH or a serial console, generates configs from templates, parses existing running-configs into structured data, runs AI-assisted operations, and enforces change discipline through an approval workflow. It is built for network engineers and MSPs who manage heterogeneous hardware and want an audit trail behind every change.

> [!NOTE]
> This project has been consolidated into **hermes-switch-manager**, which is now the actively developed repository. nethermind retains its desktop application and standalone CLI.

## Quick Start

### pip

```bash
pip install nethermind
```

### Docker (recommended)

```bash
git clone https://github.com/OneByJorah/NetCore.git
cd NetCore
cp .env.example .env   # set OPENAI_API_KEY and SSH credentials
docker compose up -d
```

Open **http://localhost:3000** for the web UI, or **http://localhost:8000/docs** for the API docs.

### From Source

```bash
git clone https://github.com/OneByJorah/NetCore.git
cd NetCore

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

## Install

### pip

```bash
pip install nethermind
```

### Docker

```bash
git clone https://github.com/OneByJorah/NetCore.git
cd NetCore
cp .env.example .env
docker compose up -d
```

### From Source

```bash
git clone https://github.com/OneByJorah/NetCore.git
cd NetCore

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Features

- **Multi-vendor support** — Cisco IOS/XR/NX-OS, HP ArubaOS-Switch (ProCurve), Juniper JunOS, Arista EOS, and Linux
- **SSH and serial console** — Netmiko for SSH, pyserial for RS-232/USB out-of-band access, plus Telnet deploy
- **50+ Jinja2 templates** — built-in configuration templates for Aruba, Cisco, and generic devices
- **Config parser** — turn existing running-config text into structured data for editing and re-rendering
- **AI chat assistant** — OpenAI-powered agent with tool calling for natural-language operations
- **IRIS-style workflow engine** — disciplined config change management with approval gates
- **Security auditing** — CVE scanning, AAA checks, and CIS/NIST compliance findings
- **Config diff and rollback** — compare versions and restore previous configs
- **Device health monitoring** — CPU, memory, and interface status metrics
- **Immutable audit trail** — every action logged with actor, target, and timestamp
- **Desktop app** — an Electron package bundles backend and frontend into one installer

## Tech Stack

- **Backend** — Python 3.12, FastAPI, SQLAlchemy, Netmiko, pyserial, Jinja2, OpenAI SDK
- **Frontend** — Next.js 16 (TypeScript), Tailwind CSS
- **Desktop** — Electron
- **Deployment** — Docker Compose, pip install
- **Database** — SQLite / PostgreSQL
- **Tooling** — uv, Ruff, pytest

## Package Badges

[![GitHub release](https://img.shields.io/github/v/release/OneByJorah/NetCore?color=009688&label=release&logo=github)](https://github.com/OneByJorah/NetCore/releases)
[![PyPI version](https://img.shields.io/pypi/v/nethermind?color=009688&label=pip&logo=pypi)](https://pypi.org/project/nethermind/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?color=FFB300&logo=open-source-initiative&logoColor=FFB300)](https://opensource.org/licenses/MIT)

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

## CLI

nethermind also ships a CLI for quick config operations:

```bash
cd scripts
python cli.py render --hostname MY-SW --mgmt-ip 192.168.1.10
python cli.py parse /path/to/running-config.txt
python cli.py deploy --transport telnet --host 192.168.1.1 --port 9023
```

## Desktop App

An Electron package bundles the backend and frontend into a single app. Build with `desktop/build-win.bat` (Windows) or `desktop/build-linux.sh` (AppImage/deb/rpm), or run from source with `npx electron .` from `desktop/`.

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
├── pyproject.toml           # Package metadata + Ruff + pytest config
├── install.sh / install.ps1
└── docs/                    # Architecture + assets
```

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), then [open an issue](https://github.com/OneByJorah/NetCore/issues) or a pull request.

## License

MIT — see [LICENSE](LICENSE).
