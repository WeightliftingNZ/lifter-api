import { CompetitionListObjectProps } from "../../interfaces";

export const COLUMNS_TO_SHOW: (keyof CompetitionListObjectProps)[] = [
  "name",
  "date_start",
  "lifts_count",
  "location",
];
