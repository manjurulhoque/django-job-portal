.DEFAULT_GOAL := dev

dev:
	python manage.py migrate && python manage.py runserver

test:
	python manage.py test

bi:
	isort . && black .

delete:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete && find . -path "*/migrations/*.pyc"  -delete

