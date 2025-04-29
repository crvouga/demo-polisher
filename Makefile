dev:
	uvicorn main:app --reload

run:
	uvicorn main:app

freeze:
	pip freeze > requirements.txt

install:
	pip install -r requirements.txt

preview:
	docker build -t demo-polisher . && docker run -p 8000:8000 demo-polisher