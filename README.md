# About
This is HTTP service on FastAPI that allows you to upload CSV files to ORM SQLite database and work with it.
# Start
Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
Installation of necessary dependencies:
```bash
pip install -r requirements.txt
```
Run server:
```bash
uvicorn main:app --reload
```
Test API:
- http://127.0.0.1:8000/docs
