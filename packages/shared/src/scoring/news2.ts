/**
 * NEWS2 Scoring Engine
 * Source: Royal College of Physicians — NEWS2, 2017
 *
 * ⚠️  PURE FUNCTION — no side effects, no randomness.
 *     Same input ALWAYS produces same output.
 *     Clinical safety: every threshold is validated by unit tests.
 */

import type { VitalSigns } from '../types/vitals';
import type { NEWS2Score, RiskBand } from '../types/risk';
import { NEWS2_CLINICAL_RESPONSES } from '../constants/news2-thresholds';

// ─── Individual Parameter Scorers ────────────────────────────────────────────

function scoreRespiratoryRate(rr: number): number {
  if (rr <= 8) return 3;
  if (rr <= 11) return 1;
  if (rr <= 20) return 0;
  if (rr <= 24) return 2;
  return 3; // >= 25
}

function scoreSpO2Scale1(spO2: number): number {
  if (spO2 <= 91) return 3;
  if (spO2 <= 93) return 2;
  if (spO2 <= 95) return 1;
  return 0; // >= 96
}

function scoreSpO2Scale2(spO2: number, onOxygen: boolean): number {
  if (spO2 <= 83) return 3;
  if (spO2 <= 85) return 2;
  if (spO2 <= 87) return 1;
  if (spO2 <= 92) return onOxygen ? 0 : 3; // 88-92: 0 on O2, 3 on air (hypoxia)
  if (!onOxygen) return 0; // >= 93 on air = 0
  // On O2, >= 93:
  if (spO2 <= 94) return 1;
  if (spO2 <= 96) return 2;
  return 3; // >= 97 on O2
}

function scoreSystolicBP(sbp: number): number {
  if (sbp <= 90) return 3;
  if (sbp <= 100) return 2;
  if (sbp <= 110) return 1;
  if (sbp <= 219) return 0;
  return 3; // >= 220
}

function scoreHeartRate(hr: number): number {
  if (hr <= 40) return 3;
  if (hr <= 50) return 1;
  if (hr <= 90) return 0;
  if (hr <= 110) return 1;
  if (hr <= 130) return 2;
  return 3; // >= 131
}

function scoreTemperature(temp: number): number {
  if (temp <= 35.0) return 3;
  if (temp <= 36.0) return 1;
  if (temp <= 38.0) return 0;
  if (temp <= 39.0) return 1;
  return 2; // >= 39.1
}

function scoreConsciousness(level: string): number {
  return level === 'A' ? 0 : 3;
}

function scoreSupplementalOxygen(onOxygen: boolean): number {
  return onOxygen ? 2 : 0;
}

// ─── Band Determination ───────────────────────────────────────────────────────

function determineBand(
  totalScore: number,
  hasAnySingleScore3: boolean,
  consciousnessNotAlert: boolean
): RiskBand {
  // CRITICAL: aggregate >= 9 OR altered consciousness with total >= 7
  if (totalScore >= 9) return 'CRITICAL';
  if (consciousnessNotAlert && totalScore >= 7) return 'CRITICAL';

  // HIGH: aggregate 7-8
  if (totalScore >= 7) return 'HIGH';

  // MEDIUM: aggregate 5-6 OR any single parameter = 3
  if (totalScore >= 5) return 'MEDIUM';
  if (hasAnySingleScore3) return 'MEDIUM';

  // LOW: everything else (0-4 with no single score of 3)
  return 'LOW';
}

// ─── Main Export ──────────────────────────────────────────────────────────────

/**
 * Calculate the NEWS2 score for a set of vital signs.
 *
 * @param vitals - Validated VitalSigns object
 * @returns NEWS2Score with total, band, individual scores, and clinical response
 */
export function calculateNEWS2(vitals: VitalSigns): NEWS2Score {
  const spO2Score = vitals.supplementalOxygen
    ? scoreSpO2Scale2(vitals.spO2, vitals.supplementalOxygen)
    : scoreSpO2Scale1(vitals.spO2);

  const individualScores: Partial<Record<keyof VitalSigns, number>> = {
    respiratoryRate: scoreRespiratoryRate(vitals.respiratoryRate),
    spO2: spO2Score,
    supplementalOxygen: scoreSupplementalOxygen(vitals.supplementalOxygen),
    systolicBP: scoreSystolicBP(vitals.systolicBP),
    heartRate: scoreHeartRate(vitals.heartRate),
    temperature: scoreTemperature(vitals.temperature),
    consciousnessLevel: scoreConsciousness(vitals.consciousnessLevel),
  };

  const totalScore = Object.values(individualScores).reduce(
    (sum, s) => sum + (s ?? 0),
    0
  );

  const hasAnySingleScore3 = Object.values(individualScores).some((s) => s === 3);
  const consciousnessNotAlert = vitals.consciousnessLevel !== 'A';

  const band = determineBand(totalScore, hasAnySingleScore3, consciousnessNotAlert);

  const triggeredParameters = Object.entries(individualScores)
    .filter(([, score]) => score !== undefined && score > 0)
    .map(([param]) => param);

  return {
    totalScore,
    band,
    individualScores,
    triggeredParameters,
    clinicalResponse: NEWS2_CLINICAL_RESPONSES[band],
    timestamp: vitals.timestamp,
  };
}
