# Pure Python mirror of packages/shared/src/scoring/news2.ts
# Deterministic — same thresholds, same logic, no side effects.

CLINICAL_RESPONSES = {
    "LOW": "Continue routine monitoring, minimum every 12 hours",
    "MEDIUM": "Urgent review by ward nurse. Increase monitoring to minimum 1-hourly",
    "HIGH": "Emergency assessment by clinical team. Continuous monitoring",
    "CRITICAL": "Immediate emergency response. Consider ICU transfer",
}


def _score_rr(rr: float) -> int:
    if rr <= 8: return 3
    if rr <= 11: return 1
    if rr <= 20: return 0
    if rr <= 24: return 2
    return 3


def _score_spo2_scale1(spo2: float) -> int:
    if spo2 <= 91: return 3
    if spo2 <= 93: return 2
    if spo2 <= 95: return 1
    return 0


def _score_spo2_scale2(spo2: float, on_o2: bool) -> int:
    if spo2 <= 83: return 3
    if spo2 <= 85: return 2
    if spo2 <= 87: return 1
    if spo2 <= 92: return 0 if on_o2 else 3
    if not on_o2: return 0
    if spo2 <= 94: return 1
    if spo2 <= 96: return 2
    return 3


def _score_sbp(sbp: float) -> int:
    if sbp <= 90: return 3
    if sbp <= 100: return 2
    if sbp <= 110: return 1
    if sbp <= 219: return 0
    return 3


def _score_hr(hr: float) -> int:
    if hr <= 40: return 3
    if hr <= 50: return 1
    if hr <= 90: return 0
    if hr <= 110: return 1
    if hr <= 130: return 2
    return 3


def _score_temp(temp: float) -> int:
    if temp <= 35.0: return 3
    if temp <= 36.0: return 1
    if temp <= 38.0: return 0
    if temp <= 39.0: return 1
    return 2


def _score_avpu(level: str) -> int:
    return 0 if level == "A" else 3


def calculate_news2(vitals: dict) -> dict:
    on_o2 = bool(vitals.get("supplementalOxygen", False))
    spo2 = float(vitals.get("spO2", 99))

    spo2_score = _score_spo2_scale2(spo2, on_o2) if on_o2 else _score_spo2_scale1(spo2)
    o2_score = 2 if on_o2 else 0

    scores = {
        "respiratoryRate": _score_rr(float(vitals.get("respiratoryRate", 16))),
        "spO2": spo2_score,
        "supplementalOxygen": o2_score,
        "systolicBP": _score_sbp(float(vitals.get("systolicBP", 120))),
        "heartRate": _score_hr(float(vitals.get("heartRate", 70))),
        "temperature": _score_temp(float(vitals.get("temperature", 37.0))),
        "consciousnessLevel": _score_avpu(str(vitals.get("consciousnessLevel", "A"))),
    }

    total = sum(scores.values())
    any_3 = any(s == 3 for s in scores.values())
    consciousness_altered = str(vitals.get("consciousnessLevel", "A")) != "A"

    if total >= 9 or (consciousness_altered and total >= 7):
        band = "CRITICAL"
    elif total >= 7:
        band = "HIGH"
    elif total >= 5 or any_3:
        band = "MEDIUM"
    else:
        band = "LOW"

    triggered = [k for k, v in scores.items() if v > 0]
    return {
        "totalScore": total,
        "band": band,
        "individualScores": scores,
        "triggeredParameters": triggered,
        "clinicalResponse": CLINICAL_RESPONSES[band],
    }
