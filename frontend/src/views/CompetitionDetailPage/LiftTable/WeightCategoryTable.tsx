/** @format */

import {
  Link,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { Link as RouterLink } from "react-router-dom";
import React from "react";
import AgeCategoryBadges from "../../../components/AgeCategoryBadges";
import LiftCells from "../../../components/LiftCells";
import { LiftObjectProps } from "../../../interfaces";
import { WeightCategoryTableProps } from "./interfaces";

const WeightCategoryTable: React.FC<WeightCategoryTableProps> = ({ lifts }) => (
  <TableContainer sx={{ maxWidth: "95vw" }}>
    <Table>
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
        {lifts.map((lift: LiftObjectProps) => (
          <TableRow
            hover
            key={lift.reference_id}
            id={`athete-${lift.reference_id}`}
          >
            <TableCell>
              {/* TODO: make tablerow a link */}
              <Link
                sx={{
                  display: "block",
                  width: "100%",
                  height: "100%",
                  m: -3,
                  p: 3,
                  textDecoration: "none",
                }}
                component={RouterLink}
                to={{
                  pathname: `/athletes/${lift.athlete}`,
                  hash: `#${lift.competition_date_start.substring(0, 4)}`,
                }}
              >
                {lift.lottery_number}
              </Link>
            </TableCell>
            <TableCell sx={{ width: 100 }}>{lift.athlete_name}</TableCell>
            <TableCell sx={{ width: 100 }}>
              <AgeCategoryBadges isColumn ageCategories={lift.age_categories} />
            </TableCell>
            <TableCell
              sx={{
                overflow: "hidden",
                textOverflow: "ellipsis",
                maxWidth: 100,
              }}
            >
              {lift.team}
            </TableCell>
            <LiftCells {...lift} />
            <TableCell align="center">
              {lift.total_lifted === 0 ? "-" : lift.total_lifted}
            </TableCell>
            <TableCell align="center">
              {lift.sinclair === 0 ? "-" : lift.total_lifted}
            </TableCell>
            <TableCell align="center">{lift.placing}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);

export default WeightCategoryTable;
