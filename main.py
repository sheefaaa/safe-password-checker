import re
import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse

app = FastAPI(title="Safe Password Checker")

@app.get("/")
def home():
    return FileResponse("index.html")

@app.get("/range/{prefix}", response_class=PlainTextResponse)
def hibp_range(prefix: str):
    if not re.fullmatch(r"[0-9A-Fa-f]{5}", prefix):
        raise HTTPException(status_code=400, detail="Invalid prefix")
    try:
        r = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix.upper()}",
            headers={"Add-Padding": "true"},
            timeout=10,
        )
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Leak service unreachable")
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Leak service error")
    return r.text