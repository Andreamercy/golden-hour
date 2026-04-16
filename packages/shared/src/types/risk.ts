import type { VitalSigns } from './vitals';

// ─── Risk Band ────────────────────────────────────────────────────────────────
export type RiskBand = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

// ─── NEWS2 Score ──────────────────────────────────────────────────────────────
export interface NEWS2Score {
  totalScore: number;
  band: RiskBand;
  /** Individual score contribution for each parameter */
  individualScores: Partial<Record<keyof VitalSigns, number>>;
  /** List of parameter names that are outside normal range */
  triggeredParameters: string[];
  /** Pre-authored clinical response instruction */
  clinicalResponse: string;
  timestamp: string;
}

// ─── MEOWS Score ──────────────────────────────────────────────────────────────
export type MEOWSColor = 'GREEN' | 'AMBER' | 'RED';

export interface MEOWSParameterResult {
  parameter: string;
  value: number | string;
  color: MEOWSColor;
  score: number;
}

export interface MEOWSScore {
  band: RiskBand;
  triggeredParameters: MEOWSParameterResult[];
  redCount: number;
  amberCount: number;
  clinicalResponse: string;
  timestamp: string;
}
