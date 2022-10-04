/** @format */

import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableRow,
} from "@mui/material";
import moment from "moment";
import React from "react";
import Heading from "../../../components/Heading";
import { AthleteDetailObjectProps } from "../../../interfaces";
import SinclairChart from "./SinclairChart";
import TableCellLink from "../../../components/TableCellLink";

interface StatsTabProps {
  athlete: AthleteDetailObjectProps;
}

function ageCategoryTitle(ageCategory: string) {
  const regex = /(\d+)( )(\d+)/;
  return ageCategory
    .replace("is_", "")
    .toLowerCase()
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ")
    .replaceAll("_", " ")
    .replace(regex, "$1-$3")
    .replace("70", "70+");
}

const StatsTab: React.FC<StatsTabProps> = ({ athlete }) => {
  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
      <SinclairChart liftSet={athlete?.lift_set} />
      <Box
        sx={{
          display: "flex",
          flexDirection: "inherit",
          gap: 2,
        }}
      >
        <Box>
          {Object.entries(athlete?.best_lifts).map(
            ([liftType, liftByAgeCategory]) => {
              return (
                <>
                  <Heading>
                    Best {liftType === "snatch" && "Snatch"}
                    {liftType === "cnj" && "Clean and Jerk"}
                    {liftType === "total" && "Total"}
                  </Heading>
                  {Object.entries(liftByAgeCategory)
                    .filter(([ageCategory]) => ageCategory !== "is_master")
                    .map(([ageCategory, liftByWeightCategory]) => (
                      <TableContainer sx={{ maxWidth: "fit-content" }}>
                        <Table padding="none">
                          <TableRow>
                            <TableCell sx={{ p: 1 }} variant="head" colSpan={4}>
                              {ageCategoryTitle(ageCategory)}
                            </TableCell>
                          </TableRow>
                          {Object.entries(liftByWeightCategory).map(
                            ([weightCategory, liftSet]) => {
                              const to = {
                                pathname: `/competitions/${liftSet.competition}`,
                                hash: liftSet.weight_category,
                              };
                              return (
                                <TableRow selected>
                                  <TableCellLink
                                    tableCellProps={{ variant: "head" }}
                                    to={to}
                                  >
                                    {weightCategory}
                                  </TableCellLink>
                                  <TableCellLink
                                    tableCellProps={{ variant: "head" }}
                                    to={to}
                                  >
                                    {liftType === "snatch" &&
                                      liftSet.best_snatch_weight[1]}
                                    {liftType === "cnj" &&
                                      liftSet.best_cnj_weight[1]}
                                    {liftType === "total" &&
                                      liftSet.total_lifted}
                                  </TableCellLink>
                                  <TableCellLink
                                    tableCellProps={{
                                      sx: {
                                        maxWidth: "300px",
                                        overflow: "hidden",
                                        textOverflow: "ellipsis",
                                      },
                                    }}
                                    to={{
                                      pathname: `/competition/${liftSet.competition}`,
                                      hash: `${liftSet.weight_category}`,
                                    }}
                                  >
                                    {liftSet.competition_name}
                                  </TableCellLink>
                                  <TableCellLink to={to}>
                                    {moment(
                                      liftSet.competition_date_start
                                    ).format("MMM Do, YYYY")}{" "}
                                    (
                                    {moment(
                                      liftSet.competition_date_start
                                    ).fromNow()}
                                    )
                                  </TableCellLink>
                                </TableRow>
                              );
                            }
                          )}
                        </Table>
                      </TableContainer>
                    ))}
                </>
              );
            }
          )}
        </Box>
        <Box>
          <Heading>Best Sinclair</Heading>
          <TableContainer sx={{ maxWidth: "fit-content" }}>
            <Table padding="none">
              <TableBody>
                {Object.entries(athlete?.best_sinclair)
                  .filter(([ageCategory]) => ageCategory !== "is_master")
                  .map(([ageCategory, liftSet]) => {
                    const to = {
                      pathname: `/competitions/${liftSet.competition}`,
                      hash: liftSet.weight_category,
                    };
                    return (
                      <TableRow selected>
                        <TableCellLink
                          to={to}
                          tableCellProps={{ variant: "head" }}
                        >
                          {ageCategoryTitle(ageCategory)}
                        </TableCellLink>
                        <TableCellLink
                          to={to}
                          tableCellProps={{ variant: "head" }}
                        >
                          {liftSet.sinclair}
                        </TableCellLink>
                        <TableCellLink to={to}>
                          {liftSet.competition_name}
                        </TableCellLink>
                        <TableCellLink to={to}>
                          {moment(liftSet.competition_date_start).format(
                            "MMM Do, YYYY"
                          )}{" "}
                          ({moment(liftSet.competition_date_start).fromNow()})
                        </TableCellLink>
                      </TableRow>
                    );
                  })}
              </TableBody>
            </Table>
          </TableContainer>
        </Box>
      </Box>
    </Box>
  );
};

export default StatsTab;
