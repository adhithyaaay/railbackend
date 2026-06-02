from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict

from models import TrainInfo, CoachPrediction, TrainAnalytics, BoardingStrategy, ExitRecommendation, RippleEffect, PlatformZone, NetworkStatus, SimulationRequest, SimulationResult
from ml_engine import simulate_predictions, generate_analytics, generate_boarding_strategy, simulate_ripple_effect, generate_exit_recommendation, generate_platform_heatmap, simulate_train_balancing, get_network_status

app = FastAPI(title="RailSense AI API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all origins for hackathon simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock train data
TRAINS = [
    TrainInfo(id="T101", name="Rajdhani Express", source="New Delhi", destination="Mumbai"),
    TrainInfo(id="T102", name="Shatabdi Express", source="Chennai", destination="Bengaluru"),
    TrainInfo(id="T103", name="Vande Bharat Express", source="Varanasi", destination="New Delhi"),
    TrainInfo(id="T104", name="Duronto Express", source="Kolkata", destination="Pune"),
    TrainInfo(id="T105", name="Tejas Express", source="Ahmedabad", destination="Mumbai"),
    TrainInfo(id="T106", name="Gatimaan Express", source="Delhi", destination="Agra"),
    TrainInfo(id="T107", name="Deccan Queen", source="Mumbai", destination="Pune"),
    TrainInfo(id="T108", name="Himalayan Queen", source="Kalka", destination="Shimla"),
]

# Cache to store latest predictions
prediction_cache: Dict[str, List[CoachPrediction]] = {}

@app.get("/api/trains", response_model=List[TrainInfo])
def get_trains():
    """Return list of available trains."""
    return TRAINS

@app.get("/api/predict/{train_id}", response_model=List[CoachPrediction])
def get_prediction(train_id: str):
    """Return prediction for 12 coaches of a specific train."""
    if train_id not in prediction_cache:
        prediction_cache[train_id] = simulate_predictions(train_id)
    return prediction_cache[train_id]

@app.get("/api/analytics/{train_id}", response_model=TrainAnalytics)
def get_analytics(train_id: str):
    """Return analytics for a specific train."""
    if train_id not in prediction_cache:
        prediction_cache[train_id] = simulate_predictions(train_id)
    return generate_analytics(prediction_cache[train_id])

@app.post("/api/refresh/{train_id}")
def refresh_predictions(train_id: str):
    """Generate new live predictions for a specific train."""
    prediction_cache[train_id] = simulate_predictions(train_id)
    return {"status": "success", "message": f"Predictions refreshed for {train_id}"}

@app.get("/api/boarding-strategy/{train_id}", response_model=BoardingStrategy)
def get_boarding_strategy(train_id: str):
    if train_id not in prediction_cache:
        prediction_cache[train_id] = simulate_predictions(train_id)
    return generate_boarding_strategy(train_id, prediction_cache[train_id])

@app.get("/api/ripple-analysis/{train_id}", response_model=RippleEffect)
def get_ripple_analysis(train_id: str):
    if train_id not in prediction_cache:
        prediction_cache[train_id] = simulate_predictions(train_id)
    return simulate_ripple_effect(prediction_cache[train_id])

@app.get("/api/platform-heatmap/{train_id}", response_model=List[PlatformZone])
def get_platform_heatmap(train_id: str):
    return generate_platform_heatmap(train_id)

@app.get("/api/exit-recommendation/{train_id}", response_model=ExitRecommendation)
def get_exit_recommendation(train_id: str):
    if train_id not in prediction_cache:
        prediction_cache[train_id] = simulate_predictions(train_id)
    return generate_exit_recommendation(prediction_cache[train_id])

@app.get("/api/network-status", response_model=NetworkStatus)
def api_network_status():
    return get_network_status()

@app.post("/api/train-balance-simulation", response_model=SimulationResult)
def train_balance_simulation(request: SimulationRequest):
    current_avg_crowd = 75
    current_avg_comfort = 4.5
    return simulate_train_balancing(request.action, request.value, current_avg_crowd, current_avg_comfort)
