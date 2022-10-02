/** @format */

export interface CompetitionCardTableProps {
  lifts: LiftObjectProps[];
}

export interface CompetitionCardProps {
  referenceId: string;
  location?: string;
  name: string;
  dateStart: string;
  dateEnd?: string;
  liftCount: number;
  liftSet: LiftObjectProps[];
}
