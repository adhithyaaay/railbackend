from pydantic import BaseModel
from typing import List, Optional, Dict

class CoachPrediction(BaseModel):
    coach: str
    crowd: int
    comfort: float
    status: str
    movement_difficulty: str
    toilet_accessibility: str
    exit_accessibility: str

class TrainAnalytics(BaseModel):
    avg_occupancy: int
    peak_hour: str
    best_coach: str
    worst_coach: str

class TrainInfo(BaseModel):
    id: str
    name: str
    source: str
    destination: str

class BoardingStrategy(BaseModel):
    recommended_zone: str
    recommended_coach: str
    walking_reduction_pct: int
    crowd_reduction_pct: int

class ExitRecommendation(BaseModel):
    fastest_exit_coach: str
    time_saved_mins: int
    exit_crowd_level: str

class RippleEffect(BaseModel):
    source_coach: str
    affected_coaches: List[str]
    risk_level: str
    message: str

class PlatformZone(BaseModel):
    zone_name: str
    crowd_density: int
    hotspot_warning: bool

class NetworkStatus(BaseModel):
    overall_congestion: str
    active_trains: int
    critical_alerts: List[str]

class SimulationRequest(BaseModel):
    action: str  # "add_coaches", "increase_frequency", "redirect_passengers"
    value: int

class SimulationResult(BaseModel):
    before_avg_crowd: int
    after_avg_crowd: int
    before_comfort: float
    after_comfort: float
    message: str
