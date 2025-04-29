dev:
	uvicorn main:app --reload

run:
	uvicorn main:app


freeze:
	pip freeze > requirements.txt
