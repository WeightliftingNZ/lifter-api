import React, { forwardRef, useMemo } from "react";
import { AgeCategoriesProps, LiftObjectProps, GradeT } from "../../interfaces";
import { useTheme } from "@mui/material/styles";
import {
  Card,
  CardContent,
  CardActionArea,
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
import {
  LinkProps as RouterLinkProps,
  Link as RouterLink,
} from "react-router-dom";

interface AthleteCardProps {
  referenceId: string;
  fullName: string;
  ageCategories: AgeCategoriesProps;
  recentLift: LiftObjectProps[];
  currentGrade: GradeT;
}

interface CardActionAreaProps {
  to: string;
  children?: React.ReactNode;
}

const CardActionAreaLink: React.FC<
  React.PropsWithChildren<CardActionAreaProps>
> = (props: CardActionAreaProps) => {
  const { to } = props;
  const renderLink = useMemo(
    () =>
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(function Link(
        itemProps,
        ref
      ) {
        return (
          <RouterLink
            to={to}
            ref={ref}
            {...itemProps}
            role={undefined}
            style={{ textDecoration: "none" }}
          />
        );
      }),
    [to]
  );
  return (
    <CardActionArea component={renderLink}>{props.children}</CardActionArea>
  );
};

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
        elevation={2}
        sx={{
          "&:hover": {
            borderColor: theme.palette.secondary.light,
            boxShadow: 2,
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
                          <>
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
                          </>
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
