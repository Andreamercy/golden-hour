import { z } from 'zod';

export const PatientIdSchema = z
  .string()
  .regex(/^PT-[A-Z0-9]{8}$/, 'Patient ID must match format PT-XXXXXXXX');

export const PatientSchema = z
  .object({
    id: PatientIdSchema,
    age: z.number({ required_error: 'Age is required' }).min(0, 'Age must be ≥ 0').max(120, 'Age must be ≤ 120'),
    sex: z.enum(['M', 'F', 'O'], { required_error: 'Sex is required' }),
    pregnancyStatus: z.boolean(),
    gestationalWeeks: z
      .number()
      .min(0, 'Gestational weeks must be ≥ 0')
      .max(42, 'Gestational weeks must be ≤ 42')
      .optional(),
    facilityId: z.string().min(1, 'Facility ID is required'),
    createdAt: z.string().datetime(),
    updatedAt: z.string().datetime(),
  })
  .refine(
    (data) => {
      if (data.pregnancyStatus && data.sex === 'M') return false;
      return true;
    },
    { message: 'Male patients cannot have pregnancy status set to true', path: ['pregnancyStatus'] }
  );

export const VitalSignsSchema = z.object({
  heartRate: z
    .number({ required_error: 'Heart rate is required', invalid_type_error: 'Heart rate must be a number' })
    .min(20, 'Heart rate must be ≥ 20 bpm')
    .max(300, 'Heart rate must be ≤ 300 bpm'),
  systolicBP: z
    .number({ required_error: 'Systolic BP is required', invalid_type_error: 'Systolic BP must be a number' })
    .min(40, 'Systolic BP must be ≥ 40 mmHg')
    .max(300, 'Systolic BP must be ≤ 300 mmHg'),
  diastolicBP: z
    .number({ required_error: 'Diastolic BP is required', invalid_type_error: 'Diastolic BP must be a number' })
    .min(20, 'Diastolic BP must be ≥ 20 mmHg')
    .max(200, 'Diastolic BP must be ≤ 200 mmHg'),
  temperature: z
    .number({ required_error: 'Temperature is required', invalid_type_error: 'Temperature must be a number' })
    .min(25, 'Temperature must be ≥ 25°C')
    .max(45, 'Temperature must be ≤ 45°C'),
  respiratoryRate: z
    .number({ required_error: 'Respiratory rate is required', invalid_type_error: 'Respiratory rate must be a number' })
    .min(1, 'Respiratory rate must be ≥ 1 breaths/min')
    .max(80, 'Respiratory rate must be ≤ 80 breaths/min'),
  spO2: z
    .number({ required_error: 'SpO2 is required', invalid_type_error: 'SpO2 must be a number' })
    .min(0, 'SpO2 must be ≥ 0%')
    .max(100, 'SpO2 must be ≤ 100%'),
  consciousnessLevel: z.enum(['A', 'V', 'P', 'U'], {
    required_error: 'Consciousness level is required',
    invalid_type_error: 'Consciousness level must be A, V, P, or U',
  }),
  supplementalOxygen: z.boolean({ required_error: 'Supplemental oxygen status is required' }),
  timestamp: z.string().datetime({ message: 'Timestamp must be a valid ISO8601 datetime' }),
  recordedBy: z.string().min(1, 'Recorded by is required'),
});

export type ValidationError = { field: string; message: string };
export type Result<T, E> = { success: true; data: T } | { success: false; errors: E };

export function validateVitals(input: unknown): Result<z.infer<typeof VitalSignsSchema>, ValidationError[]> {
  const result = VitalSignsSchema.safeParse(input);
  if (result.success) {
    return { success: true, data: result.data };
  }
  const errors: ValidationError[] = result.error.errors.map((e) => ({
    field: e.path.join('.'),
    message: e.message,
  }));
  return { success: false, errors };
}

export function validatePatient(input: unknown): Result<z.infer<typeof PatientSchema>, ValidationError[]> {
  const result = PatientSchema.safeParse(input);
  if (result.success) {
    return { success: true, data: result.data };
  }
  const errors: ValidationError[] = result.error.errors.map((e) => ({
    field: e.path.join('.'),
    message: e.message,
  }));
  return { success: false, errors };
}
