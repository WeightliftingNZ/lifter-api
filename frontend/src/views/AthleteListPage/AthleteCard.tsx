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
} from "@mui/material";
import GradeBadges from "../../components/GradeBadges";
import Heading from "../../components/Heading";
import { Stack } from "@mui/system";
import AgeCategoryBadges from "../../components/AgeCategoryBadges";
import CardActionAreaLink from "../../components/CardActionAreaLink";

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
    <>
      <Card
        variant="outlined"
        elevation={0}
        sx={{
          "&:hover": {
            borderColor: theme.palette.secondary.light,
            boxShadow: 4,
          },
        }}
      >
        <CardActionAreaLink to={`/athletes/${referenceId}`}>
          <CardContent>
            <Stack direction="column" spacing={1}>
              <Heading>{fullName}</Heading>
              <Stack direction="row" spacing={2}>
                <GradeBadges grade={currentGrade} />
                <AgeCategoryBadges ageCategories={ageCategories} />
              </Stack>
              {recentLift.length > 0 && (
                <Stack direction="column" spacing={1}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell colSpan={3}>Recent Competition</TableCell>
                        <TableCell>Sn</TableCell>
                        <TableCell>CJ</TableCell>
                        <TableCell>Total</TableCell>
                        <TableCell>Sinclair</TableCell>
                        <TableCell></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {recentLift.map((lift: LiftObjectProps) => {
                        return (
                          <TableRow key={lift.reference_id}>
                            <TableCell>{lift.competition_date_start}</TableCell>
                            <TableCell sx={{ maxWidth: 200 }}>
                              {lift.competition_name}
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

export default AthleteCard;
