/** @format */

import { useTheme } from "@mui/material/styles";
import React from "react";
import { SxProps } from "@mui/material";
import { green, red } from "@mui/material/colors";
import { LiftCellProps } from "./interfaces";
import TableCellLink from "../TableCellLink";

const LiftCell: React.FC<LiftCellProps> = ({
  isBest,
  liftStatus,
  weight,
  isEnd,
  to,
}) => {
  const veryDarkGreen = "#011202";
  const veryDarkRed = "#1c0303";

  const theme = useTheme();
  const isDarkMode = theme.palette.mode === "dark";

  const goodLiftSx: SxProps = {
    color: isDarkMode ? green[100] : green[900],
    backgroundColor: isDarkMode ? veryDarkGreen : green[200],
    borderColor: isDarkMode ? green[800] : green[400],
    textAlign: "center",
    ...(isBest && { fontWeight: "bolder", textDecoration: "underline" }),
    ...(isEnd && { borderRight: 1 }),
  };

  const noLiftSx: SxProps = {
    color: isDarkMode ? red[100] : red[900],
    backgroundColor: isDarkMode ? veryDarkRed : red[200],
    borderColor: isDarkMode ? red[800] : red[400],
    textAlign: "center",
    ...(liftStatus === "NOLIFT" && { textDecoration: "line-through" }),
    ...(isEnd && { borderRight: 1 }),
  };

  switch (liftStatus) {
    case "DNA":
      return (
        <TableCellLink to={to} tableCellProps={{ sx: noLiftSx }}>
          -
        </TableCellLink>
      );
    case "NOLIFT":
      return (
        <TableCellLink to={to} tableCellProps={{ sx: noLiftSx }}>
          {weight}
        </TableCellLink>
      );
    case "LIFT":
      return (
        <TableCellLink to={to} tableCellProps={{ sx: goodLiftSx }}>
          {weight}
        </TableCellLink>
      );
  }
};

export default LiftCell;
