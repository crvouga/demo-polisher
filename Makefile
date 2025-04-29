dev:
	uvicorn main:app --reload

run:
	uvicorn main:app
	
freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

