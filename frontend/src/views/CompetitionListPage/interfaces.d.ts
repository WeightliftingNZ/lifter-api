import { CompetitionListObjectProps } from "../../interfaces";

interface CompetitionListTableProps
  extends Omit<CompetitionListObjectProps, "date_end" | "url"> {}
