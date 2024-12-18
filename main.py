import fastapi


app = fastapi.FastAPI()



@app.post("/model")
def search_for():
    return {
            "result": "OK"
            }

@app.get("/health")
def health() -> dict[str, str]:
    return {
            "status": "OK"
            }
