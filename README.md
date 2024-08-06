# Follow
https://viblo.asia/p/fastapi-phan-1-gioi-thieu-va-setup-moi-truong-WR5JRxjQVGv
https://github.com/robert-gherlan/blog-fastapi/tree/main
https://viblo.asia/p/cai-dat-alembic-voi-sqlaichemy-trong-python-Yym40nldL91
# Docs
http://127.0.0.1:8000/redoc
http://127.0.0.1:8000/docs

# Active virtual env
`pyenv shell FastAPI`
# Run app
`uvicorn app.main:app --reload`

# Update requirements file:
`pip freeze > requirements.txt`

# Autogenerate migration
`alembic revision --autogenerate -m InitDB`

# Create 1 migration:
`alembic revision -m <message>`
# Current version database
`alembic current`
# Migration history:
`alembic history --verbose`
# Revert all migrations:
`alembic downgrade base`
# Revert migrations one by one:
`alembic downgrade -1`
# Apply all migrations:
`alembic upgrade head`
# Apply migrations one by one:
`alembic upgrade +1`
# Show all raw SQL: Ex create , delete alter ...
`alembic upgrade head --sql`
# Reset the database:
`alembic downgrade base && alembic upgrade head`