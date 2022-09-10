export interface DRFPaginatedResponseProps {
  count: number;
  next: string;
  previous: string;
  results: any[];
}

export interface CompetitionObjectProps {
  date_end: string;
  date_start: string;
  lifts_count: number;
  location: string;
  name: string;
  reference_id: string;
  url: string;
  lift_set?: LiftObjectProps[];
}

interface ageCategoriesProps {
  is_youth: boolean;
  is_junior: boolean;
  is_senior: boolean;
  is_master: boolean;
}

export interface AthleteObjectProps {
  reference_id: string;
  url: string;
  full_name: string;
  first_name: string;
  last_name: string;
  yearborn: number;
  age_categories: ageCategories;
  lift_set?: LiftObjectProps[];
}

type liftStatus = "LIFT" | "NOLIFT" | "DNA";

interface liftProps {
  lift_status: liftStatus;
  weight: number;
}

interface liftsProps {
  "1st": liftProps;
  "2nd": liftProps;
  "3rd": liftProps;
}

export interface LiftObjectProps {
  reference_id: string;
  url: string;
  lottery_number: number;
  athlete: string;
  athlete_name: string;
  athlete_yearborn: number;
  competition: string;
  competition_name: string;
  competition_date_start: string;
  snatches: liftProps;
  cnjs: liftProps;
  snatch_first: liftStatus;
  snatch_first_weight: number;
  snatch_second: liftStatus;
  snatch_second_weight: number;
  snatch_third: liftStatus;
  snatch_third_weight: number;
  cnj_first: liftStatus;
  cnj_first_weight: number;
  cnj_second: liftStatus;
  cnj_second_weight: number;
  cnj_third: liftStatus;
  cnj_third_weight: number;
  total_lifted: number;
  age_categories: ageCategoriesProps;
  bodyweight: number;
  weight_category: string;
  team: string;
  session_number: number;
  placing: string;
}
