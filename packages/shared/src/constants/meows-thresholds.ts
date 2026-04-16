/**
 * MEOWS — Modified Early Obstetric Warning Score thresholds
 * For use with pregnant patients (pregnancyStatus === true)
 */

export type MEOWSColor = 'GREEN' | 'AMBER' | 'RED';

export interface MEOWSParameter {
  color: MEOWSColor;
  score: number; // RED=2, AMBER=1, GREEN=0
}

export const MEOWS_CLINICAL_RESPONSES = {
  LOW: 'Continue routine monitoring per maternity protocol.',
  MEDIUM: 'Urgent review by midwife or obstetrician within 30 minutes.',
  HIGH: 'Immediate senior obstetric review. Prepare for possible intervention.',
  CRITICAL: 'Emergency obstetric team activation. Consider immediate delivery.',
} as const;

export function scoreSystolicBPMeows(sbp: number): MEOWSParameter {
  if (sbp < 90 || sbp >= 160) return { color: 'RED', score: 2 };
  if ((sbp >= 90 && sbp <= 100) || (sbp >= 150 && sbp <= 159)) return { color: 'AMBER', score: 1 };
  return { color: 'GREEN', score: 0 };
}

export function scoreDiastolicBPMeows(dbp: number): MEOWSParameter {
  if (dbp >= 110) return { color: 'RED', score: 2 };
  if (dbp >= 90) return { color: 'AMBER', score: 1 };
  return { color: 'GREEN', score: 0 };
}

export function scoreHeartRateMeows(hr: number): MEOWSParameter {
  if (hr < 40 || hr >= 130) return { color: 'RED', score: 2 };
  if ((hr >= 40 && hr <= 50) || (hr >= 120 && hr <= 129)) return { color: 'AMBER', score: 1 };
  return { color: 'GREEN', score: 0 };
}

export function scoreRespiratoryRateMeows(rr: number): MEOWSParameter {
  if (rr < 10 || rr >= 30) return { color: 'RED', score: 2 };
  if ((rr >= 10 && rr <= 14) || (rr >= 21 && rr <= 29)) return { color: 'AMBER', score: 1 };
  return { color: 'GREEN', score: 0 };
}

export function scoreTemperatureMeows(temp: number): MEOWSParameter {
  if (temp < 35 || temp >= 38.5) return { color: 'RED', score: 2 };
  if ((temp >= 35 && temp <= 35.4) || (temp >= 38.0 && temp <= 38.4)) return { color: 'AMBER', score: 1 };
  return { color: 'GREEN', score: 0 };
}

export function scoreSpO2Meows(spO2: number): MEOWSParameter {
  if (spO2 < 95) return { color: 'RED', score: 2 };
  if (spO2 <= 96) return { color: 'AMBER', score: 1 };
  return { color: 'GREEN', score: 0 };
}

export function scoreConsciousnessMeows(level: string): MEOWSParameter {
  if (level !== 'A') return { color: 'RED', score: 2 };
  return { color: 'GREEN', score: 0 };
}
