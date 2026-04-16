export type RiskBand = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface NEWS2Score {
  totalScore: number;
  band: RiskBand;
  individualScores: Partial<Record<string, number>>;
  triggeredParameters: string[];
  clinicalResponse: string;
  timestamp: string;
  scoreType?: 'NEWS2';
}

export interface MEOWSScore {
  totalScore: number;
  band: RiskBand;
  parameterColors: Record<string, string>;
  triggeredParameters: string[];
  clinicalResponse: string;
  timestamp: string;
  scoreType: 'MEOWS';
}

export function isMEOWS(score: NEWS2Score | MEOWSScore): score is MEOWSScore {
  return score.scoreType === 'MEOWS';
}
