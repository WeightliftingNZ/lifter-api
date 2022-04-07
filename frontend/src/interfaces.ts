export interface AthleteObject {
  reference_id: string;
  url: string;
  first_name: string;
  last_name: string;
  yearborn: number;
  full_name: string;
  is_youth: boolean;
  is_junior: boolean;
  is_senior: boolean;
  is_master: boolean;
  lift_set?: any;
}
export interface CompetitionObject {
  reference_id?: string;
  url?: string;
  competition_name?: string;
  location?: string;
  lift_count?: number;
  date_end?: string;
  date_start?: string;
  session_count?: number;
}

export interface LiftObject {
  reference_id: number;
  athlete: string;
  competition: string;
  snatch_first: string;
  snatch_first_weight: number;
  snatch_second: string;
  snatch_second_weight: number;
  snatch_third: string;
  snatch_third_weight: number;
  cnj_first: string;
  cnj_first_weight: number;
  cnj_second: string;
  cnj_second_weight: number;
  cnj_third: string;
  cnj_third_weight: number;
  bodyweight: number;
  weight_category: string;
  team: string;
  lottery_number: number;
  session_number: number;
  session_datetime: string;
}

export interface CompetitionDetailObject extends CompetitionObject {
  lift_set?: [LiftObject];
}
