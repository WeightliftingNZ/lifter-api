/** @format */

import { Collapse, IconButton, TableCell, TableRow } from "@mui/material";
import React, { useState } from "react";
import { LiftObjectProps } from "../../../interfaces";
import { printWeightCategories } from "../../../utils/customFunctions/customFunctions";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import WeightCategoryTable from "./CompetitionYearTable";
import { CompetitionYearCollapsableRowProps } from "./interfaces";

const TABLE_COL_SPAN = 15;

const CompetitionYearCollapsableRow: React.FC<
  CompetitionYearCollapsableRowProps
> = ({ groupByCompetitionYear, competitionYear }) => {
  const [open, setOpen] = useState(true);

  const handleOnClick = () => setOpen(!open);

  const lifts: LiftObjectProps[] = groupByCompetitionYear[competitionYear];
  return (
    <>
      <TableRow>
        <TableCell
          key={competitionYear}
          id={competitionYear}
          variant="head"
          colSpan={TABLE_COL_SPAN}
        >
          {competitionYear}
          <IconButton
            aria-label={`expand ${printWeightCategories(competitionYear)} row`}
            size="small"
            onClick={handleOnClick}
          >
            {open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
          </IconButton>
        </TableCell>
      </TableRow>
      <TableRow>
        <TableCell
          colSpan={TABLE_COL_SPAN}
          sx={{
            paddingBottom: 0,
            paddingTop: 0,
          }}
        >
          <Collapse in={open} timeout="auto" unmountOnExit>
            <WeightCategoryTable lifts={lifts} />
          </Collapse>
        </TableCell>
      </TableRow>
    </>
  );
};

export default CompetitionYearCollapsableRow;
