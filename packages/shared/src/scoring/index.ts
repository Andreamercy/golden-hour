import type { VitalSigns } from '../types/vitals';
import type { Patient } from '../types/patient';
import type { NEWS2Score, MEOWSScore } from '../types/risk';
import { calculateNEWS2 } from './news2';
import { calculateMEOWS } from './meows';

export { calculateNEWS2 } from './news2';
export { calculateMEOWS } from './meows';

export function calculateRisk(
  vitals: VitalSigns,
  patient: Patient
): NEWS2Score | MEOWSScore {
  if (patient.pregnancyStatus) {
    return calculateMEOWS(vitals);
  }
  return calculateNEWS2(vitals);
}
