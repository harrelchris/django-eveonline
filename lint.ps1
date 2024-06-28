.venv\Scripts\activate

black . --line-length 120

flake8 . --max-line-length 120 --extend-exclude .idea/,.venv/,*/migrations/

isort . --profile black --line-length 120
