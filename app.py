from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from textSummarizer.pipeline.prediction import PredictionPipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific frontend origins if you have them
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, or specify methods like ["GET", "POST"]
    allow_headers=["*"],  # Allow all headers, or specify headers like ["Content-Type"]
)
pipeline = PredictionPipeline()
class SummaryRequest(BaseModel):
    text: str
    maxSummaryLength: int


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


@app.get("/model/test/")
async def index():
    json_response = {
        "message": "Welcome to the Text Summarizer API. Please use the /model/predict endpoint to generate a summary."
    }
    return JSONResponse(content=json_response)


@app.post("/model/predict/")
async def generate_summary(request: SummaryRequest):
    try:
        # Extract data from the request
        text = request.text
        max_summary_length = request.maxSummaryLength
        print(f"text:{text} and max_summary_length:{max_summary_length}")

        # Perform text summarization
        # Replace `pipeline.predict(request)` with the actual prediction logic
        summary = pipeline.predict(request)

        # Return the summary as part of the response
        return JSONResponse(content={"summary": summary})

    except ValueError as ve:
        # Handle specific errors, such as invalid data values
        print(f"ValueError: {ve}")
        raise HTTPException(status_code=400, detail=f"ValueError: {ve}")

    except Exception as e:
        # Handle unexpected errors
        print(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
