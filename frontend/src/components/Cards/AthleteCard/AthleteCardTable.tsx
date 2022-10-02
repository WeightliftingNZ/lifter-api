/** @format */

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import moment from "moment";
import React from "react";
import { AthleteListObjectProps, LiftObjectProps } from "../../../interfaces";
import LiftCells from "../../LiftCells";
import SubTitle from "../../SubTitle";

const AthleteCardTable: React.FC<AthleteListObjectProps> = (athlete) => {
  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell colSpan={3}>Most Recent Competition</TableCell>
            <TableCell align="center" colSpan={3}>
              Snatch
            </TableCell>
            <TableCell align="center" colSpan={3}>
              Clean and Jerk
            </TableCell>
            <TableCell align="center">Total</TableCell>
            <TableCell align="center">Sinclair</TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {athlete.recent_lift.map((lift: LiftObjectProps) => {
            return (
              <TableRow key={lift.reference_id}>
                <TableCell>
                  {moment(lift.competition_date_start).from(moment())}
                </TableCell>
                <TableCell
                  sx={{
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    maxWidth: 100,
                  }}
                >
                  {lift.competition_name}
                </TableCell>
                <TableCell>{lift.weight_category}</TableCell>
                <LiftCells {...lift} />
                <TableCell align="center" sx={{ fontWeight: "bold" }}>
                  {lift.total_lifted === 0 ? "-" : lift.total_lifted}
                </TableCell>
                <TableCell align="center">
                  {lift.sinclair === 0 ? "-" : lift.sinclair}
                </TableCell>
                <TableCell>{lift.placing}</TableCell>
              </TableRow>
            );
          })}
          {athlete.lifts_count > 1 && (
            <TableRow>
              <TableCell colSpan={12} align="right">
                <SubTitle>
                  <>
                    {`${athlete.lifts_count - 1} more`}{" "}
                    {athlete.lifts_count - 1 > 1 ? "lifts" : "lift"}
                  </>
                </SubTitle>
              </TableCell>
            </TableRow>
          )}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default AthleteCardTable;
