import type { VitalSigns } from '../types/vitals';
import type { Patient } from '../types/patient';
import type { NEWS2Score, MEOWSScore } from '../types/risk';
import { getActionCard, type ActionCard, type ConditionType } from '../constants/action-cards';

export function detectCondition(
  vitals: VitalSigns,
  patient: Patient,
  score: NEWS2Score | MEOWSScore
): ActionCard {
  const band = score.band;
  let condition: ConditionType = 'GENERAL';

  // Neonatal: age < ~29 days (0.08 years)
  if (patient.age < 0.08) {
    condition = 'NEONATAL_DISTRESS';
  } else if (patient.pregnancyStatus) {
    // Maternal hemorrhage: tachycardia + hypotension in pregnant patient
    if (vitals.heartRate > 110 && vitals.systolicBP < 90) {
      condition = 'MATERNAL_HEMORRHAGE';
    } else if (vitals.systolicBP >= 140 || vitals.diastolicBP >= 90) {
      // Pre-eclampsia: elevated BP in pregnancy
      condition = 'MATERNAL_PREECLAMPSIA';
    }
  } else {
    // Sepsis suspect: tachycardia + fever + tachypnoea
    if (vitals.heartRate > 100 && vitals.temperature > 38 && vitals.respiratoryRate > 20) {
      condition = 'SEPSIS_SUSPECT';
    }
  }

  return getActionCard(condition, band) ?? getActionCard('GENERAL', band)!;
}
