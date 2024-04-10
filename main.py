import uvicorn
from fastapi import FastAPI

from api.endpoints import predictions

app = FastAPI(
    title="Sound Realty ML Service",
    version="1.0",
    description="API to predict house prices",
)

# Include the prediction router
app.include_router(predictions.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
