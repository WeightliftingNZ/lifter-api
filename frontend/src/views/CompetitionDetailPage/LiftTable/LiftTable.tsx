/** @format */

import { Table, TableBody, TableContainer } from "@mui/material";
import React from "react";
import { LiftObjectProps } from "../../../interfaces";
import { groupByWeightCategoryProps, LiftTableProps } from "./interfaces";
import WeightCategoryCollapsableRow from "./WeightCategoryCollapsableRow";

const LiftTable: React.FC<LiftTableProps> = ({ liftSet }) => {
  const groupByWeightCategory = liftSet.reduce(
    (
      groupByWeightCategory: groupByWeightCategoryProps,
      lift: LiftObjectProps
    ) => ({
      ...groupByWeightCategory,
      [lift.weight_category]: [
        ...(groupByWeightCategory[lift.weight_category] || []),
        lift,
      ],
    }),
    {}
  );

  return (
    <TableContainer sx={{ maxWidth: "95vw" }}>
      <Table>
        <TableBody>
          <>
            {Object.keys(groupByWeightCategory).map(
              (weightCategory: string) => (
                <WeightCategoryCollapsableRow
                  key={weightCategory}
                  weightCategory={weightCategory}
                  groupByWeightCategory={groupByWeightCategory}
                />
              )
            )}
          </>
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default LiftTable;
