/** @format */

import React from "react";
import { AgeCategoriesProps, LiftObjectProps, GradeT } from "../../interfaces";
import { useTheme } from "@mui/material/styles";
import {
  Card,
  CardContent,
  Table,
  TableHead,
  TableRow,
  TableBody,
  TableCell,
  CardHeader,
  Box,
  TableContainer,
  Button,
} from "@mui/material";
import GradeBadges from "../../components/GradeBadges";
import AgeCategoryBadges from "../../components/AgeCategoryBadges";
import CardActionAreaLink from "../../components/CardActionAreaLink";
import moment from "moment";
import LiftCells from "../LiftCells";

interface AthleteCardProps {
  referenceId: string;
  fullName: string;
  ageCategories: AgeCategoriesProps;
  recentLift: LiftObjectProps[];
  currentGrade: GradeT;
}

const AthleteCard: React.FC<AthleteCardProps> = ({
  fullName,
  ageCategories,
  currentGrade,
  recentLift,
  referenceId,
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
          boxShadow: 4,
        },
      }}
    >
      <CardActionAreaLink to={`/athletes/${referenceId}`}>
        <CardHeader
          title={fullName}
          subheader={
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                width: "fit-content",
              }}
            >
              <GradeBadges grade={currentGrade} />
              <AgeCategoryBadges ageCategories={ageCategories} />
            </Box>
          }
        />
      </CardActionAreaLink>
      <CardContent>
        {recentLift.length > 0 && (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell colSpan={3}></TableCell>
                  <TableCell align="center" colSpan={3}>
                    Snatch
                  </TableCell>
                  <TableCell align="center" colSpan={3}>
                    Clean and Jerk
                  </TableCell>
                  <TableCell>Total</TableCell>
                  <TableCell>Sinclair</TableCell>
                  <TableCell></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {recentLift.map((lift: LiftObjectProps) => {
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

export default AthleteCard;
