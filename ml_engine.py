import random
from datetime import datetime
from typing import List, Dict, Any
from models import CoachPrediction, TrainAnalytics

def get_status_from_crowd(crowd: int) -> str:
    if crowd < 50:
        return "Comfortable"
    elif crowd < 80:
        return "Moderate"
    else:
        return "Crowded"

def get_comfort_from_crowd(crowd: int) -> float:
    # 0 crowd -> 10 comfort
    # 100 crowd -> 1 comfort
    comfort = 10.0 - (crowd / 100.0) * 9.0
    return round(max(1.0, comfort), 1)

def simulate_predictions(train_id: str) -> List[CoachPrediction]:
    """
    Simulate ML prediction logic for 12 coaches.
    Morning peak = more crowded
    Middle coaches = more crowded
    Weekend = moderate crowd
    """
    now = datetime.now()
    hour = now.hour
    is_weekend = now.weekday() >= 5
    
    predictions = []
    
    # Base crowd depends on time
    if 7 <= hour <= 10 or 17 <= hour <= 20:
        base_crowd = 70 if not is_weekend else 50
    else:
        base_crowd = 40 if not is_weekend else 60
        
    for i in range(1, 13):
        coach_name = f"C{i}"
        
        # Middle coaches (C4-C8) usually more crowded
        if 4 <= i <= 8:
            coach_modifier = random.randint(10, 25)
        else:
            coach_modifier = random.randint(-20, 5)
            
        crowd_pct = base_crowd + coach_modifier
        # Add some random noise
        crowd_pct += random.randint(-10, 10)
        
        # Clamp to 0-100
        crowd_pct = max(0, min(100, crowd_pct))
        
        status = get_status_from_crowd(crowd_pct)
        comfort = get_comfort_from_crowd(crowd_pct)
        
        movement_difficulty = "Easy" if crowd_pct < 40 else ("Moderate" if crowd_pct < 70 else ("Difficult" if crowd_pct < 90 else "Severe"))
        toilet_accessibility = "Good" if crowd_pct < 60 else "Poor"
        exit_accessibility = "Good" if crowd_pct < 75 else "Poor"
        
        predictions.append(
            CoachPrediction(
                coach=coach_name,
                crowd=crowd_pct,
                comfort=comfort,
                status=status,
                movement_difficulty=movement_difficulty,
                toilet_accessibility=toilet_accessibility,
                exit_accessibility=exit_accessibility
            )
        )
        
    return predictions

def generate_analytics(predictions: List[CoachPrediction]) -> TrainAnalytics:
    if not predictions:
        return TrainAnalytics(
            avg_occupancy=0,
            peak_hour="N/A",
            best_coach="N/A",
            worst_coach="N/A"
        )
        
    avg_occ = sum(p.crowd for p in predictions) // len(predictions)
    best_coach = min(predictions, key=lambda x: x.crowd).coach
    worst_coach = max(predictions, key=lambda x: x.crowd).coach
    
    now = datetime.now()
    hour = now.hour
    is_weekend = now.weekday() >= 5
    
    if is_weekend:
        peak_hour = "12 PM"
    else:
        peak_hour = "6 PM" if hour >= 12 else "9 AM"
        
    return TrainAnalytics(
        avg_occupancy=avg_occ,
        peak_hour=peak_hour,
        best_coach=best_coach,
        worst_coach=worst_coach
    )

def generate_boarding_strategy(train_id: str, predictions: List[CoachPrediction]) -> Dict[str, Any]:
    if not predictions:
        return {}
    # Find least crowded coach
    best_coach = min(predictions, key=lambda p: p.crowd)
    
    # Simple zone mapping: C1-C4 -> Zone A, C5-C8 -> Zone B, C9-C12 -> Zone C
    idx = int(best_coach.coach[1:])
    zone = "Zone A" if idx <= 4 else ("Zone B" if idx <= 8 else "Zone C")
    
    return {
        "recommended_zone": zone,
        "recommended_coach": best_coach.coach,
        "walking_reduction_pct": random.randint(15, 45),
        "crowd_reduction_pct": random.randint(20, 60)
    }

def simulate_ripple_effect(predictions: List[CoachPrediction]) -> Dict[str, Any]:
    # Find the most crowded coach
    if not predictions:
        return {}
    
    worst_coach = max(predictions, key=lambda p: p.crowd)
    idx = int(worst_coach.coach[1:])
    
    affected = []
    if idx > 1: affected.append(f"C{idx-1}")
    if idx < 12: affected.append(f"C{idx+1}")
    
    risk_level = "High" if worst_coach.crowd > 85 else ("Medium" if worst_coach.crowd > 70 else "Low")
    
    return {
        "source_coach": worst_coach.coach,
        "affected_coaches": affected,
        "risk_level": risk_level,
        "message": f"Spillover expected from {worst_coach.coach} into adjacent coaches."
    }

def generate_exit_recommendation(predictions: List[CoachPrediction]) -> Dict[str, Any]:
    if not predictions:
        return {}
    # Find best exit coach based on lowest crowd and good exit accessibility
    best_exits = [p for p in predictions if p.exit_accessibility == "Good"]
    if not best_exits:
        best_exits = predictions
    best_exit = min(best_exits, key=lambda p: p.crowd)
    
    return {
        "fastest_exit_coach": best_exit.coach,
        "time_saved_mins": random.randint(3, 12),
        "exit_crowd_level": best_exit.status
    }

def generate_platform_heatmap(train_id: str) -> List[Dict[str, Any]]:
    # Mocking zones A, B, C
    return [
        {"zone_name": "Zone A", "crowd_density": random.randint(20, 90), "hotspot_warning": random.choice([True, False])},
        {"zone_name": "Zone B", "crowd_density": random.randint(20, 90), "hotspot_warning": random.choice([True, False])},
        {"zone_name": "Zone C", "crowd_density": random.randint(20, 90), "hotspot_warning": random.choice([True, False])}
    ]

def simulate_train_balancing(action: str, value: int, current_avg_crowd: int, current_avg_comfort: float) -> Dict[str, Any]:
    after_crowd = current_avg_crowd
    after_comfort = current_avg_comfort
    
    if action == "add_coaches":
        reduction = min(current_avg_crowd - 10, value * 5)
        after_crowd = max(10, current_avg_crowd - reduction)
        after_comfort = min(10.0, current_avg_comfort + (reduction / 10.0))
        message = f"Adding {value} coaches reduced crowding effectively."
    elif action == "increase_frequency":
        reduction = min(current_avg_crowd - 20, value * 10)
        after_crowd = max(10, current_avg_crowd - reduction)
        after_comfort = min(10.0, current_avg_comfort + (reduction / 10.0))
        message = f"Increasing frequency by {value} trains/hr significantly improved comfort."
    else:
        message = "Unknown action, no simulation effect."
        
    return {
        "before_avg_crowd": current_avg_crowd,
        "after_avg_crowd": after_crowd,
        "before_comfort": round(current_avg_comfort, 1),
        "after_comfort": round(after_comfort, 1),
        "message": message
    }

def get_network_status() -> Dict[str, Any]:
    risk = random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])
    return {
        "overall_congestion": risk,
        "active_trains": random.randint(45, 120),
        "critical_alerts": [
            "Platform 3 overloaded -> Redirect passengers",
            "Delays expected on Western Line"
        ] if risk in ["HIGH", "CRITICAL"] else []
    }
