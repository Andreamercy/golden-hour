"""Unit tests for the NEWS2 scoring engine (Python mirror)."""
import pytest
from src.scoring import calculate_news2, determine_risk_band


def make_vitals(**overrides):
    """Helper: build a valid vitals dict with healthy defaults."""
    defaults = {
        "heart_rate": 75,
        "systolic_bp": 120,
        "diastolic_bp": 80,
        "temperature": 37.0,
        "respiratory_rate": 16,
        "spo2": 97,
        "consciousness_level": "A",
        "supplemental_oxygen": False,
    }
    defaults.update(overrides)
    return defaults


class TestNEWS2Scoring:
    def test_normal_healthy_adult_is_low(self):
        result = calculate_news2(make_vitals())
        assert result["total_score"] == 0
        assert result["band"] == "LOW"

    def test_tachycardia_scores_correctly(self):
        # HR 131+ = score 3
        result = calculate_news2(make_vitals(heart_rate=135))
        assert result["individual_scores"]["heart_rate"] == 3

    def test_bradycardia_scores_3(self):
        # HR <=40 = score 3
        result = calculate_news2(make_vitals(heart_rate=38))
        assert result["individual_scores"]["heart_rate"] == 3

    def test_low_bp_scores_3(self):
        # systolic <=90 = score 3
        result = calculate_news2(make_vitals(systolic_bp=85))
        assert result["individual_scores"]["systolic_bp"] == 3

    def test_high_bp_scores_3(self):
        # systolic >=220 = score 3
        result = calculate_news2(make_vitals(systolic_bp=225))
        assert result["individual_scores"]["systolic_bp"] == 3

    def test_low_spo2_on_air_scores_3(self):
        result = calculate_news2(make_vitals(spo2=89, supplemental_oxygen=False))
        assert result["individual_scores"]["spo2"] == 3

    def test_sepsis_like_vitals_critical(self):
        result = calculate_news2(make_vitals(
            heart_rate=135,
            systolic_bp=85,
            temperature=39.8,
            respiratory_rate=30,
            spo2=89,
            consciousness_level="V"
        ))
        assert result["band"] == "CRITICAL"
        assert result["total_score"] >= 9

    def test_unconscious_patient_critical(self):
        result = calculate_news2(make_vitals(consciousness_level="U"))
        assert result["individual_scores"]["consciousness"] == 3
        # Even if total score is low, AVPU != A should trigger escalation
        assert result["band"] in ("MEDIUM", "HIGH", "CRITICAL")

    def test_single_parameter_score_3_elevates_to_medium(self):
        # Only HR is abnormal (score 3), total = 3 -> should be MEDIUM not LOW
        result = calculate_news2(make_vitals(heart_rate=135))
        assert result["band"] == "MEDIUM"

    def test_score_5_is_medium(self):
        # RR 21-24 = 2, HR 91-110 = 1, Temp 38.1-39.0 = 1, SpO2 94-95 = 1 -> total 5
        result = calculate_news2(make_vitals(
            respiratory_rate=22,
            heart_rate=95,
            temperature=38.5,
            spo2=94
        ))
        assert result["total_score"] == 5
        assert result["band"] == "MEDIUM"

    def test_score_7_is_high(self):
        band = determine_risk_band(7, False)
        assert band == "HIGH"

    def test_score_9_is_critical(self):
        band = determine_risk_band(9, False)
        assert band == "CRITICAL"

    def test_spo2_scale2_on_oxygen(self):
        # SpO2 97% on supplemental O2 = score 3 (Scale 2: >=97 on O2)
        result = calculate_news2(make_vitals(spo2=97, supplemental_oxygen=True))
        assert result["individual_scores"]["spo2"] == 3

    def test_supplemental_oxygen_adds_score(self):
        result = calculate_news2(make_vitals(supplemental_oxygen=True, spo2=97))
        assert result["individual_scores"]["supplemental_oxygen"] == 2

    def test_clinical_response_present(self):
        result = calculate_news2(make_vitals())
        assert "clinical_response" in result
        assert len(result["clinical_response"]) > 0

    def test_triggered_parameters_listed(self):
        result = calculate_news2(make_vitals(heart_rate=135, systolic_bp=85))
        assert "heart_rate" in result["triggered_parameters"]
        assert "systolic_bp" in result["triggered_parameters"]

    def test_hr_boundary_40(self):
        assert calculate_news2(make_vitals(heart_rate=40))["individual_scores"]["heart_rate"] == 3

    def test_hr_boundary_41(self):
        assert calculate_news2(make_vitals(heart_rate=41))["individual_scores"]["heart_rate"] == 1

    def test_hr_boundary_50(self):
        assert calculate_news2(make_vitals(heart_rate=50))["individual_scores"]["heart_rate"] == 1

    def test_hr_boundary_51(self):
        assert calculate_news2(make_vitals(heart_rate=51))["individual_scores"]["heart_rate"] == 0

    def test_hr_boundary_90(self):
        assert calculate_news2(make_vitals(heart_rate=90))["individual_scores"]["heart_rate"] == 0

    def test_hr_boundary_91(self):
        assert calculate_news2(make_vitals(heart_rate=91))["individual_scores"]["heart_rate"] == 1

    def test_hr_boundary_110(self):
        assert calculate_news2(make_vitals(heart_rate=110))["individual_scores"]["heart_rate"] == 1

    def test_hr_boundary_111(self):
        assert calculate_news2(make_vitals(heart_rate=111))["individual_scores"]["heart_rate"] == 2

    def test_hr_boundary_130(self):
        assert calculate_news2(make_vitals(heart_rate=130))["individual_scores"]["heart_rate"] == 2

    def test_hr_boundary_131(self):
        assert calculate_news2(make_vitals(heart_rate=131))["individual_scores"]["heart_rate"] == 3
