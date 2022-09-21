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
  Box,
} from "@mui/material";
import Heading from "../../components/Heading";
import { Stack } from "@mui/system";
import CardActionAreaLink from "../../components/CardActionAreaLink";
import CompetitionBadges from "../../components/CompetitionBadges";
import SubTitle from "../../components/SubTitle";
import Body from "../../components/Body";
import moment from "moment";

interface CompetitionCardProps {
  referenceId: string;
  name: string;
  dateStart: string;
  dateEnd: string;
  liftCount: number;
  randomLifts: LiftObjectProps[];
}

const CompetitionCard: React.FC<CompetitionCardProps> = ({
  referenceId,
  name,
  dateStart,
  dateEnd,
  liftCount,
  randomLifts,
}) => {
  const theme = useTheme();
  return (
    <>
      <Card
        variant="outlined"
        elevation={2}
        sx={{
          "&:hover": {
            borderColor: theme.palette.secondary.light,
            boxShadow: 2,
          },
        }}
      >
        <CardActionAreaLink to={`/competitions/${referenceId}`}>
          <CardContent>
            <Stack direction="column" spacing={1}>
              <Heading>{name}</Heading>
              <Stack direction="row" spacing={2}>
                <CompetitionBadges name={name} />
              </Stack>
              <Box>
                <Body>
                  {moment(dateStart).format("dddd, Do MMM YYYY")}{" "}
                  {dateStart !== dateEnd &&
                    `- ${moment(dateEnd).format("dddd, Do MMM YYYY")}`}
                </Body>
                <SubTitle>Number of Athletes: {liftCount}</SubTitle>
              </Box>
              {randomLifts.length > 0 && (
                <Stack direction="column" spacing={1}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell colSpan={2}>Lifts</TableCell>
                        <TableCell>Sn</TableCell>
                        <TableCell>CJ</TableCell>
                        <TableCell>Total</TableCell>
                        <TableCell>Sinclair</TableCell>
                        <TableCell></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {randomLifts.map((lift: LiftObjectProps) => {
                        return (
                          <TableRow>
                            <TableCell sx={{ maxWidth: 200 }}>
                              {lift.athlete_name}
                            </TableCell>
                            <TableCell>{lift.weight_category}</TableCell>
                            <TableCell>{lift.best_snatch_weight[1]}</TableCell>
                            <TableCell>{lift.best_cnj_weight[1]}</TableCell>
                            <TableCell>{lift.total_lifted}</TableCell>
                            <TableCell>{lift.sinclair}</TableCell>
                            <TableCell>{lift.placing}</TableCell>
                          </TableRow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </Stack>
              )}
            </Stack>
          </CardContent>
        </CardActionAreaLink>
      </Card>
    </>
  );
};

export default CompetitionCard;
