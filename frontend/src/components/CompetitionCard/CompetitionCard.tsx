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
  TableContainer,
  CardHeader,
  Divider,
  Button,
} from "@mui/material";
import CardActionAreaLink from "../../components/CardActionAreaLink";
import moment from "moment";
import LiftCells from "../../components/LiftCells";
import { Box } from "@mui/system";
/* import CompetitionBadges from "../../components/CompetitionBadges"; */

interface CompetitionCardProps {
  referenceId: string;
  location?: string;
  name: string;
  dateStart: string;
  dateEnd?: string;
  liftCount: number;
  randomLifts: LiftObjectProps[];
}

const CompetitionCard: React.FC<CompetitionCardProps> = ({
  referenceId,
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
        <CardHeader
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
        />
      </CardActionAreaLink>
      <CardContent>
        {randomLifts.length > 0 && (
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
                  <TableCell>Total</TableCell>
                  <TableCell>Sinclair</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {randomLifts.map((lift: LiftObjectProps) => {
                  return (
                    <TableRow key={lift.reference_id}>
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
        )}
        {/* <Button size="large" color="secondary"> */}
        {/*   Share */}
        {/* </Button> */}
        <Button size="large" color="secondary">
          See more
        </Button>
      </CardContent>
    </Card>
  );
};

export default CompetitionCard;
