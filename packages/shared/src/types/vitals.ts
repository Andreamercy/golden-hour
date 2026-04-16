import { z } from 'zod';

export const VitalSignsSchema = z.object({
  heartRate: z
    .number()
    .min(20, 'Heart rate must be 20-300 bpm')
    .max(300, 'Heart rate must be 20-300 bpm'),
  systolicBP: z
    .number()
    .min(40, 'Systolic BP must be 40-300 mmHg')
    .max(300, 'Systolic BP must be 40-300 mmHg'),
  diastolicBP: z
    .number()
    .min(20, 'Diastolic BP must be 20-200 mmHg')
    .max(200, 'Diastolic BP must be 20-200 mmHg'),
  temperature: z
    .number()
    .min(25, 'Temperature must be 25-45 °C')
    .max(45, 'Temperature must be 25-45 °C'),
  respiratoryRate: z
    .number()
    .min(1, 'Respiratory rate must be 1-80 breaths/min')
    .max(80, 'Respiratory rate must be 1-80 breaths/min'),
  spO2: z
    .number()
    .min(0, 'SpO2 must be 0-100 %')
    .max(100, 'SpO2 must be 0-100 %'),
  consciousnessLevel: z.enum(['A', 'V', 'P', 'U'], {
    errorMap: () => ({ message: 'Consciousness level must be A, V, P, or U (AVPU scale)' }),
  }),
  supplementalOxygen: z.boolean(),
  timestamp: z.string().datetime('Timestamp must be a valid ISO 8601 datetime'),
  recordedBy: z.string().min(1, 'Health worker ID is required'),
});

export type VitalSigns = z.infer<typeof VitalSignsSchema>;
