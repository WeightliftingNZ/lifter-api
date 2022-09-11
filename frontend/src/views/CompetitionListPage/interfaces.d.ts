import { CompetitionObjectProps } from "../../interfaces";

interface CompetitionListTableProps
  extends Omit<CompetitionObjectProps, "date_end" | "url"> {}
