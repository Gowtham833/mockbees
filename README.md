# MockBees

<!-- GitHub Actions CI badge -->
[![CI](https://github.com/Gowtham833/mockbees/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Gowtham833/mockbees/actions/workflows/ci.yml)

<!-- Vercel deploy badge (replace ORG/PROJECT with your Vercel org and project) -->
[![Vercel](https://vercel.com/ORG/PROJECT/deployments/badge)](https://vercel.com/ORG/PROJECT)

Lightweight AI-powered mock test platform. See `DEPLOYMENT.md` for deployment and local development instructions.

## Tech Stack

### Frontend
- **Framework**: [React 18](https://reactjs.org/) (bootstrapped with [Vite](https://vitejs.dev/))
- **State Management**: [Zustand](https://github.com/pmndrs/zustand)
- **Routing**: [React Router](https://reactrouter.com/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **Charts**: [Recharts](https://recharts.org/)
- **Styling & UI**: Custom CSS, React Icons, React Hot Toast

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Database Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Authentication**: JWT, Passlib (Bcrypt)
- **AI Integration**: [Groq API](https://groq.com/)

### Deployment & CI/CD
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Render
- **CI/CD**: GitHub Actions
