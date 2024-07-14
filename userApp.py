from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from textSummarizer.pipeline.prediction import PredictionPipeline
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific frontend origins if you have them
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, or specify methods like ["GET", "POST"]
    allow_headers=["*"],  # Allow all headers, or specify headers like ["Content-Type"]
)

# Initialize PredictionPipeline once at startup
pipeline = PredictionPipeline()


@app.get("/model/test/")
async def index():
    json_response = {
        "message": "Welcome to the Text Summarizer API. Please use the /model/predict endpoint to generate a summary."
    }
    return JSONResponse(content=json_response)


# @app.post("/model/predict/")
# async def generate_summary(request: SummaryRequest):
#     try:
#         # Ensure summaryLength is positive
#         if request.summaryLength <= 0:
#             raise HTTPException(status_code=400, detail="summaryLength must be a positive integer")

#         print(request)
#         # Generate summary
#         summarized_text = "Hello world"
#         return {"summary": summarized_text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


class SummaryRequest(BaseModel):
    text: str
    maxSummaryLength: int


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
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
