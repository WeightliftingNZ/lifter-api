/** @format */

export interface DRFPaginatedResponseProps {
  count: number;
  next: string;
  previous: string;
  per_page: number;
  results: any[];
}

interface BaseSearchResultProps {
  query_result_headline: string;
  query_result_headline_no_html: string;
}

interface CompetitionSearchResultProps extends BaseSearchResultProps {
  query_result_type: "Competition";
  query_result: CompetitionListObjectProps;
}

interface AthleteSearchResultProps extends BaseSearchResultProps {
  query_result_type: "Athlete";
  query_result: AthleteListObjectProps;
}

interface LiftSearchResultProps extends BaseSearchResultProps {
  query_result_type: "Lift";
  query_result: LiftObjectProps;
}

export type SearchResultProps =
  | LiftSearchResultProps
  | AthleteSearchResultProps
  | CompetitionSearchResultProps;

export interface CompetitionListObjectProps {
  date_end: string;
  date_start: string;
  lifts_count: number;
  best_lifts: LiftObjectProps[];
  location: string;
  name: string;
  reference_id: string;
  url: string;
  competition_last_edited: string;
  lift_last_edited?: string;
}

export interface CompetitionDetailObjectProps
  extends CompetitionListObjectProps {
  lift_set: LiftObjectProps[];
}

interface AgeCategoriesProps {
  is_youth: boolean;
  is_junior: boolean;
  is_senior: boolean;
  is_master: boolean;
  is_master_35_39: boolean;
  is_master_35_39: boolean;
  is_master_40_44: boolean;
  is_master_45_49: boolean;
  is_master_50_54: boolean;
  is_master_55_59: boolean;
  is_master_60_64: boolean;
  is_master_65_69: boolean;
  is_master_70: boolean;
}

export type GradeT =
  | "Elite"
  | "International"
  | "A"
  | "B"
  | "C"
  | "D"
  | "E"
  | null;

export interface AthleteListObjectProps {
  reference_id: string;
  url: string;
  full_name: string;
  first_name: string;
  last_name: string;
  yearborn: number;
  lifts_count: number;
  athlete_last_edited: string;
  lift_last_edited?: string;
  current_grade: GradeT;
  age_categories: ageCategories;
  recent_lift: LiftObjectProps[];
}

export interface AthleteDetailObjectProps extends AthleteListObjectProps {
  lift_set: LiftObjectProps[];
  best_sinclair: { [key: string]: LiftObjectProps };
  best_lifts: {
    snatch: { [key: string]: { [key: string]: LiftObjectProps } };
    cnj: { [key: string]: { [key: string]: LiftObjectProps } };
    total: { [key: string]: { [key: string]: LiftObjectProps } };
  };
}

type liftStatus = "LIFT" | "NOLIFT" | "DNA";

interface liftProps {
  lift_status: liftStatus;
  weight: number;
}

export interface LiftsProps {
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
  competition_date_start: string; // YYYY-MM-DD
  snatches: liftProps;
  cnjs: liftProps;
  snatch_first: liftStatus;
  snatch_first_weight: number;
  snatch_second: liftStatus;
  snatch_second_weight: number;
  snatch_third: liftStatus;
  snatch_third_weight: number;
  best_snatch_weight: [string, number];
  cnj_first: liftStatus;
  cnj_first_weight: number;
  cnj_second: liftStatus;
  cnj_second_weight: number;
  cnj_third: liftStatus;
  cnj_third_weight: number;
  best_cnj_weight: [string, number];
  total_lifted: number;
  sinclair: number;
  age_categories: AgeCategoriesProps;
  grade: GradeT;
  bodyweight: number;
  weight_category: string;
  team: string;
  session_number: number;
  placing: string;
}
