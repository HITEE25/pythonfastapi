from fastapi import FastAPI
import pandas as pd
from fastapi.responses import StreamingResponse

print("JSON APP LOADED")

app = FastAPI()

@app.get("/")
def home():
    return {"message": "home"}

@app.get("/json")
def get_json():
    df = pd.DataFrame(
        [["canada",10],["india",100]],
        columns=["team","points"]
    )
    return df.to_dict(orient="records")

from io import BytesIO # Add to Top of File
@app.get("/xlsx")
def get_excel_data():
    df = pd.DataFrame(
        [["Canada", 10], ["USA", 20]], 
        columns=["team", "points"]
    )
    buffer = BytesIO()
    with pd.ExcelWriter(buffer) as writer:
        df.to_excel(writer, index=False)
    return StreamingResponse(
        BytesIO(buffer.getvalue()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": f"inline; filename=data.csv"}
)

from fastapi.responses import HTMLResponse

@app.get("/table", response_class=HTMLResponse)
def get_table():
    df = pd.DataFrame(
        [["Canada", 10], ["USA", 20]],
        columns=["team", "points"]
    )
    return df.to_html(index=False)