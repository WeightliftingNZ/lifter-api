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
import { CompetitionYearTableProps } from "./interfaces";
import moment from "moment";
import TableCellLink from "../../../components/TableCellLink";

const CompetitionYearTable: React.FC<CompetitionYearTableProps> = ({
  lifts,
}) => (
  <TableContainer sx={{ maxWidth: "95vw" }}>
    <Table size="small" padding="none">
      <TableHead>
        <TableRow>
          <TableCell align="center" colSpan={2}>
            Competition
          </TableCell>
          <TableCell align="center">Team</TableCell>
          <TableCell align="center">Weight Cat.</TableCell>
          <TableCell align="center" colSpan={3}>
            Snatch
          </TableCell>
          <TableCell align="center" colSpan={3}>
            Clean and Jerk
          </TableCell>
          <TableCell align="center">Total</TableCell>
          <TableCell align="center">Sinclair</TableCell>
          <TableCell align="center" colSpan={2}>
            Place
          </TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {lifts.map((lift: LiftObjectProps) => {
          const to = {
            pathname: `/competitions/${lift.competition}`,
            hash: lift.weight_category,
          };
          return (
            <TableRow
              hover
              key={lift.reference_id}
              id={`lift-${lift.reference_id}`}
            >
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
                {lift.competition_name}
              </TableCellLink>
              <TableCellLink to={to}>
                {moment(lift.competition_date_start).format("ddd, Do MMM")}
              </TableCellLink>
              <TableCellLink
                to={to}
                tableCellProps={{
                  sx: {
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    Width: 100,
                  },
                }}
              >
                {lift.team}
              </TableCellLink>
              <TableCellLink to={to} tableCellProps={{ align: "center" }}>
                {lift.weight_category}
              </TableCellLink>
              <LiftCells to={to} {...lift} />
              <TableCellLink to={to} tableCellProps={{ align: "center" }}>
                {lift.total_lifted === 0 ? "-" : lift.total_lifted}
              </TableCellLink>
              <TableCellLink to={to} tableCellProps={{ align: "center" }}>
                {lift.sinclair === 0 ? "-" : lift.sinclair}
              </TableCellLink>
              <TableCellLink to={to} tableCellProps={{ align: "center" }}>
                {lift.placing}
              </TableCellLink>
              <TableCellLink to={to} sx={{ maxWidth: 100 }}>
                <AgeCategoryBadges
                  isColumn
                  ageCategories={lift.age_categories}
                />
              </TableCellLink>
            </TableRow>
          );
        })}
      </TableBody>
    </Table>
  </TableContainer>
);

export default CompetitionYearTable;
