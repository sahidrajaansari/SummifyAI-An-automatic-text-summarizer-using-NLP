from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from textSummarizer.pipeline.prediction import PredictionPipeline

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize PredictionPipeline once at startup
pipeline = PredictionPipeline()


class TextRequest(BaseModel):
    text: str
    summary_length: int


@app.get("/")
async def index():
    return RedirectResponse(url="/static/index.html")


@app.post("/predict")
async def predict_route(request: TextRequest):
    try:
        # Separate summary_length and text
        summary_length = request.summary_length
        text = request.text

        print(f"Summary Length: {summary_length}, Text: {text}")
        
        # Call predict method with separated inputs
        summarized_text = pipeline.predict(str(request))
        return {"summarized_text": summarized_text}
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {e}")
        # Return a user-friendly error message
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)