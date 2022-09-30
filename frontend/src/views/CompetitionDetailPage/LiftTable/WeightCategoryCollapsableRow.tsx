/** @format */

import { Collapse, IconButton, TableCell, TableRow } from "@mui/material";
import React, { useState } from "react";
import { LiftObjectProps } from "../../../interfaces";
import { printWeightCategories } from "../../../utils/customFunctions/customFunctions";
import { TABLE_COL_SPAN } from "./constants";
import { WeightCategoryCollapsableRowProps } from "./interfaces";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import WeightCategoryTable from "./WeightCategoryTable";

const WeightCategoryCollapsableRow: React.FC<
  WeightCategoryCollapsableRowProps
> = ({ groupByWeightCategory, weightCategory }) => {
  const [open, setOpen] = useState(true);

  const handleOnClick = () => setOpen(!open);

  const lifts: LiftObjectProps[] = groupByWeightCategory[weightCategory];
  return (
    <>
      <TableRow>
        <TableCell
          key={weightCategory}
          id={weightCategory}
          variant="head"
          colSpan={TABLE_COL_SPAN}
        >
          {printWeightCategories(weightCategory)}
          <IconButton
            aria-label={`expand ${printWeightCategories(weightCategory)} row`}
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

export default WeightCategoryCollapsableRow;
