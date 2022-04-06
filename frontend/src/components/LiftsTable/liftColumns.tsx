import React from "react";
import { Link } from "react-router-dom";

// provides logic for displaying weights lifted
// a bolded lift means the lift was made and was the best lift
// a strike thorough means the lift was attempted and a no lift
// a "-" means the lift was not declared or attempted
const displayWeightCell = ({ cell }: { cell: any }) => {
  let bolded = false;
  const arrayLiftType = cell.column.id.split(".");
  let bestLift = "";
  if (arrayLiftType[0] === "snatches") {
    bestLift = cell.row.original.best_snatch_weight[0];
  } else if (arrayLiftType[0] === "cnjs") {
    bestLift = cell.row.original.best_cnj_weight[0];
  }
  if (arrayLiftType[1] === bestLift) {
    bolded = true;
  }
  return (
    <div className={bolded ? "font-bold" : ""}>
      <div
        className={cell.value.lift_status === "NOLIFT" ? "line-through" : ""}
      >
        {cell.value.lift_status === "DNA" ? "-" : cell.value.weight}
      </div>
    </div>
  );
};

export const liftColumns = [
  {
    Header: "No.",
    accessor: "lottery_number",
  },
  {
    Header: "Name",
    accessor: "athlete_name",
    Cell: ({ cell }: { cell: any }) => {
      return (
        <Link to={`/athletes/${cell.row.original.athlete}`}>
          <div className="text-left text-blue-600 font-semibold underline">
            {cell.value}
          </div>
        </Link>
      );
    },
  },
  {
    Header: "Born",
    accessor: "athlete_yearborn",
  },
  {
    Header: "Cat.",
    accessor: "weight_category",
  },
  {
    Header: "Team",
    accessor: "team",
    Cell: ({ cell }: { cell: any }) => {
      return <div className="pr-2">{cell.value}</div>;
    },
  },
  {
    Header: "Snatch",
    columns: [
      {
        Header: "1",
        accessor: "snatches.1st",
        Cell: displayWeightCell,
      },
      {
        Header: "2",
        accessor: "snatches.2nd",
        Cell: displayWeightCell,
      },
      {
        Header: "3",
        accessor: "snatches.3rd",
        Cell: displayWeightCell,
      },
    ],
  },
  {
    Header: "Clean & Jerk",
    columns: [
      {
        Header: "1",
        accessor: "cnjs.1st",
        Cell: displayWeightCell,
      },
      {
        Header: "2",
        accessor: "cnjs.2nd",
        Cell: displayWeightCell,
      },
      {
        Header: "3",
        accessor: "cnjs.3rd",
        Cell: displayWeightCell,
      },
    ],
    Cell: ({ cell }: { cell: any }) => {
      return <h1>{cell.value.weight}</h1>;
    },
  },
  {
    Header: "Results",
    columns: [
      {
        Header: "Sn",
        accessor: "best_snatch_weight.1",
      },
      {
        Header: "CJ",
        accessor: "best_cnj_weight.1",
      },
      {
        Header: "T",
        accessor: "total_lifted",
      },
    ],
  },
  {
    Header: "Placing",
    accessor: "placing",
  },
];
