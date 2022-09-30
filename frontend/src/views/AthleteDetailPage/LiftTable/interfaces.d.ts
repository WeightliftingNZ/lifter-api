/** @format */

import LiftObjectProps from "../../../interfaces";

export interface LiftTableProps {
  liftSet: LiftObjectProps[];
}

export interface groupByCompetitionYearProps {
  [key: string]: LiftObjectProps[];
}

export interface CompetitionYearTableProps {
  lifts: LiftObjectProps[];
}

export interface CompetitionYearCollapsableRowProps {
  competitionYear: string;
  groupByCompetitionYear: groupByCompetitionYearProps;
}

export interface liftSetIncludingCompetitionYearProps extends LiftObjectProps {
  competitionYear: number;
}
