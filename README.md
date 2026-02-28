# Sistema de Gestão Acadêmica (Multi-tenant)

Scaffold inicial para um sistema de gestão escolar multi-tenant com RBAC.

Stack: FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT (local)

- Cada escola é um `tenant`.
- Identificação de tenant por header `X-Tenant-ID` ou path `/t/{tenant_id}`.

Para começar:

1. Ative o venv: `source venv/bin/activate`
2. Instale dependências: `pip install -r requirements.txt`
3. Defina `DATABASE_URL` e `SECRET_KEY` em `.env`
4. Rode migrations com alembic
5. Execute: `uvicorn app.main:app --reload`
