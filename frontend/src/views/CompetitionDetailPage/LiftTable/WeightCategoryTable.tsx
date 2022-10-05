/** @format */

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import React from "react";
import AgeCategoryBadges from "../../../components/AgeCategoryBadges";
import LiftCells from "../../../components/LiftCells";
import { LiftObjectProps } from "../../../interfaces";
import { WeightCategoryTableProps } from "./interfaces";
import TableCellLink from "../../../components/TableCellLink";

const WeightCategoryTable: React.FC<WeightCategoryTableProps> = ({ lifts }) => (
  <TableContainer sx={{ maxWidth: "95vw" }}>
    <Table size="small" padding="none">
      <TableHead>
        <TableRow>
          <TableCell align="center">Lott.</TableCell>
          <TableCell align="center" colSpan={2}>
            Name
          </TableCell>
          <TableCell align="center">Team</TableCell>
          <TableCell align="center" colSpan={3}>
            Snatch
          </TableCell>
          <TableCell align="center" colSpan={3}>
            Clean and Jerk
          </TableCell>
          <TableCell align="center">Total</TableCell>
          <TableCell align="center">Sinclair</TableCell>
          <TableCell align="center">Place</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {lifts.map((lift: LiftObjectProps) => {
          const to = {
            pathname: `/athletes/${lift.athlete}`,
            hash: `${lift.competition_date_start.substring(0, 4)}`,
          };

          return (
            <TableRow
              hover
              key={lift.reference_id}
              id={`athete-${lift.reference_id}`}
            >
              <TableCellLink to={to}>{lift.lottery_number}</TableCellLink>
              <TableCellLink to={to} tableCellProps={{ sx: { width: 100 } }}>
                {lift.athlete_name}
              </TableCellLink>
              <TableCellLink to={to} tableCellProps={{ sx: { width: 100 } }}>
                <AgeCategoryBadges
                  isColumn
                  ageCategories={lift.age_categories}
                />
              </TableCellLink>
              <TableCellLink
                to={to}
                tableCellProps={{
                  sx: {
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    maxWidth: 100,
                  },
                }}
              >
                {lift.team}
              </TableCellLink>
              <LiftCells to={to} {...lift} />
              <TableCellLink to={to} tableCellProps={{ align: "center" }}>
                {lift.total_lifted === 0 ? "-" : lift.total_lifted}
              </TableCellLink>
              <TableCellLink to={to} tableCellProps={{ align: "center" }}>
                {lift.sinclair === 0 ? "-" : lift.total_lifted}
              </TableCellLink>
              <TableCellLink to={to} tableCellProps={{ align: "center" }}>
                {lift.placing}
              </TableCellLink>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  </TableContainer>
);

export default WeightCategoryTable;
