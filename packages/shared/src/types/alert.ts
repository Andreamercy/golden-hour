import { z } from 'zod';
import type { NEWS2Score, MEOWSScore } from './risk';

export const AlertSchema = z.object({
  id: z.string().uuid(),
  patientId: z.string().regex(/^PT-[A-Z0-9]{8}$/, 'Invalid patient ID format'),
  score: z.any(), // NEWS2Score | MEOWSScore — runtime union
  facilityId: z.string().min(1),
  gpsLatitude: z.number().min(-90).max(90),
  gpsLongitude: z.number().min(-180).max(180),
  sentVia: z.array(z.enum(['SMS', 'PUSH', 'DASHBOARD'])),
  acknowledged: z.boolean(),
  acknowledgedBy: z.string().nullable(),
  createdAt: z.string().datetime(),
});

export type Alert = {
  id: string;
  patientId: string;
  score: NEWS2Score | MEOWSScore;
  facilityId: string;
  gpsLatitude: number;
  gpsLongitude: number;
  sentVia: ('SMS' | 'PUSH' | 'DASHBOARD')[];
  acknowledged: boolean;
  acknowledgedBy: string | null;
  createdAt: string;
};
