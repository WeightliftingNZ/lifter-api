/** @format */

import { Table, TableBody, TableContainer } from "@mui/material";
import React from "react";
import {
  groupByCompetitionYearProps,
  liftSetIncludingCompetitionYearProps,
  LiftTableProps,
} from "./interfaces";
import CompetitionYearCollapsableRow from "./CompetitionYearCollapsableRow";

const LiftTable: React.FC<LiftTableProps> = ({ liftSet }) => {
  const liftSetIncludingCompetitionYear: liftSetIncludingCompetitionYearProps[] =
    liftSet.map((lift) => {
      const year = lift.competition_date_start.substring(0, 4);
      return {
        ...lift,
        competitionYear: year,
      };
    });

  const groupByCompetitionYear = liftSetIncludingCompetitionYear.reduce(
    (
      groupByCompetitionYear: groupByCompetitionYearProps,
      lift: liftSetIncludingCompetitionYearProps
    ) => ({
      ...groupByCompetitionYear,
      [lift.competitionYear]: [
        ...(groupByCompetitionYear[lift.competitionYear] || []),
        lift,
      ],
    }),
    {}
  );

  return (
    <TableContainer sx={{ maxWidth: "95vw" }}>
      <Table size="small">
        <TableBody>
          <>
            {Object.keys(groupByCompetitionYear)
              .reverse()
              .map((competitionYear: string) => (
                <CompetitionYearCollapsableRow
                  key={competitionYear}
                  competitionYear={competitionYear}
                  groupByCompetitionYear={groupByCompetitionYear}
                />
              ))}
          </>
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default LiftTable;
