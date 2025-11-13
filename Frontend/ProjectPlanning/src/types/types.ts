export type CoverageRequest = "DINERO" | "MATERIALES" | "MANO_DE_OBRA";
export type StatusStage = "PENDING" | "IN_PROGRESS" | "FINISHED";
export type Status = 'PENDING' | 'IN_PROGRESS' | 'RESOLVED';

export interface Observation {
  id: number;
  project_id: number;
  project_name: string | null;
  name: string;
  description: string | null;
  status: Status;
}


export interface Stage {
  id: number;
  id_project: number;
  name: string;
  description: string | null;
  start_date: string | null;
  end_date: string | null;
  coverage_request: CoverageRequest;
  requires_contribution: boolean;
  status: StatusStage;
}

export interface Project {
  id: number;
  user_id: number;
  name: string;
  description: string;
  stages: Stage[];
}

export type ApiError = 
  | { type: 'SESSION_EXPIRED'; message: string }
  | { type: 'PERMISSION_DENIED'; message: string }
  | { type: 'NETWORK_ERROR'; message: string }
  | { type: 'UNKNOWN_ERROR'; message: string }
  | { type: 'NOT_FOUND'; message:string }
  | { type: 'CONFLICT'; message:string};