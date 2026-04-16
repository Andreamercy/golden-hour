/**
 * MEOWS Scoring Engine — Modified Early Obstetric Warning Score
 * Used for pregnant patients instead of NEWS2.
 */

import type { VitalSigns } from '../types/vitals';
import type { MEOWSScore, RiskBand } from '../types/risk';
import {
  scoreSystolicBPMeows,
  scoreDiastolicBPMeows,
  scoreHeartRateMeows,
  scoreRespiratoryRateMeows,
  scoreTemperatureMeows,
  scoreSpO2Meows,
  scoreConsciousnessMeows,
  MEOWS_CLINICAL_RESPONSES,
  type MEOWSColor,
} from '../constants/meows-thresholds';

export function calculateMEOWS(vitals: VitalSigns): MEOWSScore {
  const parameters = {
    systolicBP: scoreSystolicBPMeows(vitals.systolicBP),
    diastolicBP: scoreDiastolicBPMeows(vitals.diastolicBP),
    heartRate: scoreHeartRateMeows(vitals.heartRate),
    respiratoryRate: scoreRespiratoryRateMeows(vitals.respiratoryRate),
    temperature: scoreTemperatureMeows(vitals.temperature),
    spO2: scoreSpO2Meows(vitals.spO2),
    consciousnessLevel: scoreConsciousnessMeows(vitals.consciousnessLevel),
  };

  const colors: Record<string, MEOWSColor> = {};
  const triggeredParameters: string[] = [];

  for (const [key, param] of Object.entries(parameters)) {
    colors[key] = param.color;
    if (param.color !== 'GREEN') triggeredParameters.push(key);
  }

  const hasRed = Object.values(parameters).some((p) => p.color === 'RED');
  const amberCount = Object.values(parameters).filter((p) => p.color === 'AMBER').length;

  let band: RiskBand;
  if (hasRed) {
    band = 'CRITICAL';
  } else if (amberCount >= 2) {
    band = 'HIGH';
  } else if (amberCount === 1) {
    band = 'MEDIUM';
  } else {
    band = 'LOW';
  }

  return {
    totalScore: Object.values(parameters).reduce((s, p) => s + p.score, 0),
    band,
    parameterColors: colors,
    triggeredParameters,
    clinicalResponse: MEOWS_CLINICAL_RESPONSES[band],
    timestamp: vitals.timestamp,
    scoreType: 'MEOWS',
  };
}
