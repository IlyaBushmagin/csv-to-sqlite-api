from fastapi import FastAPI, File, UploadFile, HTTPException
from sqlalchemy import create_engine, text
from io import BytesIO
import pandas as pd

app = FastAPI(
    title='CSV to SQLite API'
)

engine = create_engine('sqlite://', echo=False)
tables = {}

@app.get('/')
def docs_url():
    return 'Go to API docs: http://127.0.0.1:8000/docs'

@app.get('/describe')
def get_tables():
    return tables

@app.get('/select')
def get_data(query: str):

    if not query.lower().startswith('select'):
        raise HTTPException(400, detail='Select statement error')

    with engine.connect() as conn:
        try:
            out = conn.execute(text(query)).fetchall()
        except Exception:
            raise HTTPException(400, detail='Select statement error')
        
    res = {}
    for row in out:
        res[row[0]] = row[1:]

    return res

@app.get('/drop')
def drop_table(table: str):

    if table not in tables:
        raise HTTPException(400, detail='Table does not exist')
    else:
        del tables[table]
    
    with engine.connect() as conn:
        conn.execute(text('drop table ' + table))

    return {'dropped': table}

@app.post('/upload_csv')
def create_table(csv_file: UploadFile = File(...)):
    
    if csv_file.content_type != 'text/csv':
        raise HTTPException(400, detail='File type error')
    
    filename = csv_file.filename[:-4]
    contents = csv_file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer)
    df.to_sql(name=filename, con=engine, if_exists='replace')
    tables[filename] = list(df.columns)

    buffer.close()
    csv_file.file.close()

    return {'created': filename}
