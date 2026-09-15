install:
	pip install -r requirements.txt

run-api:
	uvicorn main:app --reload

run-dashboard:
	streamlit run streamlit_app/app.py

test:
	pytest -q

evaluate:
	python evaluation/run_evaluation.py

generate-data:
	python scripts/generate_synthetic.py
