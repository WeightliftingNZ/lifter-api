/** @format */

import React from "react";
import { LiftObjectProps } from "../../interfaces";
import {
  Table,
  TableHead,
  TableRow,
  TableBody,
  TableCell,
  TableContainer,
  Divider,
  Alert,
} from "@mui/material";
import moment from "moment";
import LiftCells from "../../components/LiftCells";
import { Box } from "@mui/system";
/* import CompetitionBadges from "../../components/CompetitionBadges"; */
import CustomCard from "../../components/CustomCard";

interface CompetitionCardProps {
  referenceId: string;
  location?: string;
  name: string;
  dateStart: string;
  dateEnd?: string;
  liftCount: number;
  liftSet: LiftObjectProps[];
}

interface CompetitionCardTableProps {
  lifts: LiftObjectProps[];
}

const CompetitionCardTable: React.FC<CompetitionCardTableProps> = ({
  lifts,
}) => {
  return (
    <TableContainer sx={{ overflowX: "scroll", maxWidth: "95vw" }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell colSpan={4}></TableCell>
            <TableCell align="center" colSpan={3}>
              Snatch
            </TableCell>
            <TableCell align="center" colSpan={3}>
              Clean and Jerk
            </TableCell>
            <TableCell align="center">Total</TableCell>
            <TableCell align="center">Sinclair</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {lifts.map((lift: LiftObjectProps) => {
            return (
              <TableRow hover key={lift.reference_id}>
                <TableCell>{lift.placing}</TableCell>
                <TableCell sx={{ maxWidth: 100 }}>
                  {lift.athlete_name}
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
                <TableCell>{lift.weight_category}</TableCell>
                <LiftCells {...lift} />
                <TableCell align="center" sx={{ fontWeight: "bold" }}>
                  {lift.total_lifted === 0 ? "-" : lift.total_lifted}
                </TableCell>
                <TableCell align="center">
                  {lift.sinclair === 0 ? "-" : lift.sinclair}
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

const CompetitionCard: React.FC<CompetitionCardProps> = ({
  referenceId,
  name,
  dateStart,
  liftCount,
  liftSet,
}) => {
  return (
    <CustomCard
      actionLink={`/competitions/${referenceId}`}
      title={name}
      subheader={
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            width: "fit-content",
            borderRadius: 1,
            color: "text.secondary",
            "& hr": {
              mx: 1,
            },
          }}
        >
          {moment(dateStart).from(moment())}
          <Divider orientation="vertical" variant="fullWidth" flexItem />
          {liftCount} {liftCount > 1 ? "athletes" : "athlete"}
        </Box>
      }
      contents={
        liftSet.length > 0 ? (
          <CompetitionCardTable lifts={liftSet} />
        ) : (
          <Alert severity="info">Pending results</Alert>
        )
      }
    />
  );
};

export default CompetitionCard;
