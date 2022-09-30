/** @format */

import { useTheme } from "@mui/material/styles";
import React from "react";
import { SxProps, TableCell } from "@mui/material";
import { green, red } from "@mui/material/colors";
import { LiftCellProps } from "./interfaces";

const LiftCell: React.FC<LiftCellProps> = (
  { isBest, liftStatus, weight, isEnd },
  props
) => {
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
      return <TableCell sx={noLiftSx}>-</TableCell>;
    case "NOLIFT":
      return <TableCell sx={noLiftSx}>{weight}</TableCell>;
    case "LIFT":
      return <TableCell sx={goodLiftSx}>{weight}</TableCell>;
  }
};

export default LiftCell;
