/** @format */

import { TableCellProps } from "@mui/material";

export interface LiftCellProps extends TableCellProps {
  isEnd?: boolean;
  isBest: boolean;
  liftStatus: "LIFT" | "NOLIFT" | "DNA";
  weight: number;
  to?: string | { pathname: string; hash: string };
}
