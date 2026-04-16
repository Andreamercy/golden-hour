import { z } from 'zod';

// ─── Branded PatientId ────────────────────────────────────────────────────────
const patientIdRegex = /^PT-[A-Z0-9]{8}$/;

export const PatientIdSchema = z
  .string()
  .regex(patientIdRegex, 'Patient ID must match format PT-XXXXXXXX (alphanumeric)');

export type PatientId = z.infer<typeof PatientIdSchema>;

// ─── Patient ──────────────────────────────────────────────────────────────────
export const PatientSchema = z
  .object({
    id: PatientIdSchema,
    age: z.number().int().min(0, 'Age must be 0 or above').max(120, 'Age must be 120 or below'),
    sex: z.enum(['M', 'F', 'O'], { errorMap: () => ({ message: 'Sex must be M, F, or O' }) }),
    pregnancyStatus: z.boolean(),
    gestationalWeeks: z
      .number()
      .int()
      .min(0, 'Gestational weeks must be 0 or above')
      .max(42, 'Gestational weeks must be 42 or below')
      .optional(),
    facilityId: z.string().min(1, 'Facility ID is required'),
    createdAt: z.string().datetime('createdAt must be a valid ISO 8601 datetime'),
    updatedAt: z.string().datetime('updatedAt must be a valid ISO 8601 datetime'),
  })
  .refine(
    (data) => {
      if (data.pregnancyStatus && data.gestationalWeeks === undefined) {
        return false;
      }
      return true;
    },
    {
      message: 'gestationalWeeks is required when pregnancyStatus is true',
      path: ['gestationalWeeks'],
    }
  );

export type Patient = z.infer<typeof PatientSchema>;
