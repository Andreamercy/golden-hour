/**
 * NEWS2 Scoring Thresholds
 * Source: Royal College of Physicians — National Early Warning Score 2 (NEWS2), 2017
 * https://www.rcplondon.ac.uk/projects/outputs/national-early-warning-score-news-2
 *
 * ⚠️  CLINICAL SAFETY: Do NOT modify these values without verifying against the
 *     RCP specification. An incorrect threshold could affect clinical decisions.
 */

/** Respiratory Rate scoring (breaths/min) */
export const RR_THRESHOLDS = [
  { max: 8, score: 3 },
  { min: 9, max: 11, score: 1 },
  { min: 12, max: 20, score: 0 },
  { min: 21, max: 24, score: 2 },
  { min: 25, score: 3 },
] as const;

/** SpO2 Scale 1 — for patients NOT on supplemental oxygen (breaths/min) */
export const SPO2_SCALE1_THRESHOLDS = [
  { max: 91, score: 3 },
  { min: 92, max: 93, score: 2 },
  { min: 94, max: 95, score: 1 },
  { min: 96, score: 0 },
] as const;

/**
 * SpO2 Scale 2 — for patients WITH supplemental oxygen (e.g., COPD target range)
 * Use Scale 2 ONLY when clinically indicated AND patient is on O2.
 */
export const SPO2_SCALE2_THRESHOLDS = [
  { max: 83, score: 3 },
  { min: 84, max: 85, score: 2 },
  { min: 86, max: 87, score: 1 },
  // 88-92 on O2 = 0; >=93 on air = 0
  { min: 88, max: 92, onOxygen: true, score: 0 },
  { min: 93, onOxygen: false, score: 0 },
  // On O2 above 92:
  { min: 93, max: 94, onOxygen: true, score: 1 },
  { min: 95, max: 96, onOxygen: true, score: 2 },
  { min: 97, onOxygen: true, score: 3 },
] as const;

/** Systolic BP scoring (mmHg) */
export const SYSTOLIC_BP_THRESHOLDS = [
  { max: 90, score: 3 },
  { min: 91, max: 100, score: 2 },
  { min: 101, max: 110, score: 1 },
  { min: 111, max: 219, score: 0 },
  { min: 220, score: 3 },
] as const;

/** Heart Rate scoring (bpm) */
export const HEART_RATE_THRESHOLDS = [
  { max: 40, score: 3 },
  { min: 41, max: 50, score: 1 },
  { min: 51, max: 90, score: 0 },
  { min: 91, max: 110, score: 1 },
  { min: 111, max: 130, score: 2 },
  { min: 131, score: 3 },
] as const;

/** Temperature scoring (°C) */
export const TEMPERATURE_THRESHOLDS = [
  { max: 35.0, score: 3 },
  { min: 35.1, max: 36.0, score: 1 },
  { min: 36.1, max: 38.0, score: 0 },
  { min: 38.1, max: 39.0, score: 1 },
  { min: 39.1, score: 2 },
] as const;

/** NEWS2 Risk Band thresholds */
export const NEWS2_BAND_THRESHOLDS = {
  /** Aggregate score 0-4 with no single parameter score of 3 */
  LOW_MAX: 4,
  /** Aggregate 5-6 OR any single parameter = 3 */
  MEDIUM_MIN: 5,
  MEDIUM_MAX: 6,
  /** Aggregate 7+ */
  HIGH_MIN: 7,
  /** Aggregate 9+ OR consciousness ≠ A with score ≥ 7 */
  CRITICAL_MIN: 9,
} as const;

/** Clinical response text for each risk band (pre-authored, not generative) */
export const NEWS2_CLINICAL_RESPONSES = {
  LOW: 'Continue routine monitoring. Minimum reassessment every 12 hours.',
  MEDIUM:
    'Urgent review by ward nurse. Increase monitoring to a minimum of 1-hourly. Inform the responsible clinician.',
  HIGH: 'Emergency assessment by a clinical team with core competencies in the care of acutely ill patients. Continuous monitoring of vital signs.',
  CRITICAL:
    'Immediate emergency response. Emergency assessment by a team with critical care competencies. Consider transfer to a higher level of care (ICU/HDU).',
} as const;
