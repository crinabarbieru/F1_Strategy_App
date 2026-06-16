VALID_COMPOUNDS = ("soft", "medium", "hard")

# Seconds lost per lap, compared to a fresh soft tire for each compound type
COMPOUND_BASE_DELTA = {
    "soft":   0.0,
    "medium": 0.6,
    "hard":   1.2,
}

# Seconds of degradation per lap for each compound type
COMPOUND_DEGRADATION = {
    "soft":   0.12,
    "medium": 0.07,
    "hard":   0.04,
}

# Maximum tire age (laps) for each compound type
MAX_TIRE_AGE = {
    "soft":   25,
    "medium": 40,
    "hard":   55,
}

PIT_STOP_TIME_LOSS = 22.0