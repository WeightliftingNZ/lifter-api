/** @format */

import React from "react";
import { LiftObjectProps } from "../../interfaces";
import { useTheme } from "@mui/material/styles";
import {
  Card,
  CardContent,
  Table,
  TableHead,
  TableRow,
  TableBody,
  TableCell,
  TableCellProps,
  Box,
  SxProps,
  Typography,
  TableContainer,
  CardHeader,
} from "@mui/material";
import Heading from "../../components/Heading";
import { Stack } from "@mui/system";
import CardActionAreaLink from "../../components/CardActionAreaLink";
import CompetitionBadges from "../../components/CompetitionBadges";
import SubTitle from "../../components/SubTitle";
import Body from "../../components/Body";
import moment from "moment";
import { green, red } from "@mui/material/colors";

interface CompetitionCardProps {
  referenceId: string;
  location: string;
  name: string;
  dateStart: string;
  dateEnd?: string;
  liftCount: number;
  randomLifts: LiftObjectProps[];
}

const HeaderTableCell: React.FC<TableCellProps> = (props: TableCellProps) => {
  return (
    <TableCell align="center" {...props}>
      <Typography variant="overline">{props.children}</Typography>
    </TableCell>
  );
};

const NormalTableCell: React.FC<TableCellProps> = (props: TableCellProps) => {
  return (
    <TableCell {...props}>
      <Typography variant="body1" sx={{ fontWeight: "inherit" }}>
        {props.children}
      </Typography>
    </TableCell>
  );
};

interface LiftCellProps {
  isBest: boolean;
  liftStatus: "LIFT" | "NOLIFT" | "DNA";
  weight: number;
}

const LiftCell: React.FC<LiftCellProps> = ({ isBest, liftStatus, weight }) => {
  const theme = useTheme();
  const isDarkMode = theme.palette.mode === "dark";

  const veryDarkGreen = "#011202";
  const veryDarkRed = "#1c0303";

  const goodLiftSx: SxProps = {
    color: isDarkMode ? green[100] : green[900],
    backgroundColor: isDarkMode ? veryDarkGreen : green[200],
    borderColor: isDarkMode ? green[800] : green[400],
    textAlign: "center",
    ...(isBest && { fontWeight: "bolder", borderWidth: 3 }),
  };

  const noLiftSx: SxProps = {
    color: isDarkMode ? red[100] : red[900],
    backgroundColor: isDarkMode ? veryDarkRed : red[200],
    borderColor: isDarkMode ? red[800] : red[400],
    textAlign: "center",
    ...(liftStatus === "NOLIFT" && { textDecoration: "line-through" }),
  };

  switch (liftStatus) {
    case "DNA":
      return <NormalTableCell sx={noLiftSx}>-</NormalTableCell>;
    case "NOLIFT":
      return <NormalTableCell sx={noLiftSx}>{weight}</NormalTableCell>;
    case "LIFT":
      return <NormalTableCell sx={goodLiftSx}>{weight}</NormalTableCell>;
  }
};

const LiftCells: React.FC<LiftObjectProps> = ({
  best_snatch_weight,
  best_cnj_weight,
  snatch_first,
  snatch_first_weight,
  snatch_second,
  snatch_second_weight,
  snatch_third,
  snatch_third_weight,
  cnj_first,
  cnj_first_weight,
  cnj_second,
  cnj_second_weight,
  cnj_third,
  cnj_third_weight,
}) => {
  const best_snatch = best_snatch_weight[0];
  const best_cnj = best_cnj_weight[0];

  return (
    <>
      <LiftCell
        isBest={best_snatch === "1st"}
        liftStatus={snatch_first}
        weight={snatch_first_weight}
      />
      <LiftCell
        isBest={best_snatch === "2nd"}
        liftStatus={snatch_second}
        weight={snatch_second_weight}
      />
      <LiftCell
        isBest={best_snatch === "3rd"}
        liftStatus={snatch_third}
        weight={snatch_third_weight}
      />
      <LiftCell
        isBest={best_cnj === "1st"}
        liftStatus={cnj_first}
        weight={cnj_first_weight}
      />
      <LiftCell
        isBest={best_cnj === "2nd"}
        liftStatus={cnj_second}
        weight={cnj_second_weight}
      />
      <LiftCell
        isBest={best_cnj === "3rd"}
        liftStatus={cnj_third}
        weight={cnj_third_weight}
      />
    </>
  );
};

const CompetitionCard: React.FC<CompetitionCardProps> = ({
  referenceId,
  location,
  name,
  dateStart,
  liftCount,
  randomLifts,
}) => {
  const theme = useTheme();
  return (
    <Card
      variant="outlined"
      elevation={0}
      sx={{
        maxWidth: "100vw",
        "&:hover": {
          borderColor: theme.palette.secondary.light,
          boxShadow: 2,
        },
      }}
    >
      <CardActionAreaLink to={`/competitions/${referenceId}`}>
        <CardContent>
          <CardHeader></CardHeader>
          <Stack direction="column" spacing={1}>
            <Heading>{name}</Heading>
            <Stack direction="row" spacing={2}>
              <CompetitionBadges name={name} />
            </Stack>
            <Box>
              <Body>{moment(dateStart).from(moment())}</Body>
              <SubTitle>{location}</SubTitle>
              <SubTitle>{liftCount} Athletes</SubTitle>
            </Box>
            {randomLifts.length > 0 && (
              <Stack direction="column" spacing={1}>
                <TableContainer sx={{ overflowX: "scroll", maxWidth: "95vw" }}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <HeaderTableCell colSpan={4}></HeaderTableCell>
                        <HeaderTableCell colSpan={3}>Snatch</HeaderTableCell>
                        <HeaderTableCell colSpan={3}>
                          Clean and Jerk
                        </HeaderTableCell>
                        <HeaderTableCell>Total</HeaderTableCell>
                        <HeaderTableCell>Sinclair</HeaderTableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {randomLifts.map((lift: LiftObjectProps) => {
                        return (
                          <TableRow key={lift.reference_id}>
                            <NormalTableCell>{lift.placing}</NormalTableCell>
                            <NormalTableCell sx={{ maxWidth: 100 }}>
                              {lift.athlete_name}
                            </NormalTableCell>
                            <TableCell
                              sx={{
                                overflow: "hidden",
                                textOverflow: "ellipsis",
                                maxWidth: 100,
                              }}
                            >
                              {lift.team}
                            </TableCell>
                            <NormalTableCell>
                              {lift.weight_category}
                            </NormalTableCell>
                            <LiftCells {...lift} />
                            <NormalTableCell
                              align="center"
                              sx={{ fontWeight: "bold" }}
                            >
                              {lift.total_lifted === 0
                                ? "-"
                                : lift.total_lifted}
                            </NormalTableCell>
                            <NormalTableCell align="center">
                              {lift.sinclair === 0 ? "-" : lift.sinclair}
                            </NormalTableCell>
                          </TableRow>
                        );
                      })}
                      <TableRow>
                        <TableCell>...</TableCell>
                        <TableCell colSpan={12}></TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </TableContainer>
              </Stack>
            )}
          </Stack>
        </CardContent>
      </CardActionAreaLink>
    </Card>
  );
};

export default CompetitionCard;
