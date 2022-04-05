import React, { useMemo, useState } from "react";
import { useTable } from "react-table";
import { useQuery } from "react-query";
import { Link } from "react-router-dom";
import apiClient from "../../utils/http-common/http-common";
import Loading from "../Loading";
import Error from "../Error";

const LiftsTable = ({ competitionId, sessionId }: any) => {
  const [session, setSession] = useState({ lift_set: [] });
  const { isLoading, isError } = useQuery(
    ["session", sessionId],
    async () => {
      return await apiClient.get(
        `/competitions/${competitionId}/sessions/${sessionId}`
      );
    },
    {
      enabled: Boolean(sessionId),
      onSuccess: (res) => {
        const result = {
          status: res.status + "-" + res.statusText,
          headers: res.headers,
          data: res.data,
        };
        setSession(result.data);
      },
      onError: (err) => {
        console.log(err);
      },
    }
  );

  const lifts = session.lift_set;

  const isEven = (idx: number) => idx % 2 !== 0;

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

  const liftData = useMemo(() => [...lifts], [lifts]);

  const liftColumns = useMemo(
    () => [
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
    ],
    []
  );

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns: liftColumns, data: liftData } as any);

  if (isLoading) {
    return (
      <>
        <Loading />
      </>
    );
  }
  if (isError) {
    return (
      <>
        <Error />
      </>
    );
  }
  if (lifts.length === 0) {
    return <div>No lifts!</div>;
  }
  return (
    <div className="flex self-center">
      <table {...getTableProps}>
        <thead>
          {headerGroups.map((headerGroup, idx) => (
            <tr {...headerGroup.getHeaderGroupProps()} key={idx}>
              {headerGroup.headers.map((column, idx) => (
                <th {...column.getHeaderProps()} key={idx}>
                  {column.render("Header")}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row, idx) => {
            prepareRow(row);
            return (
              <tr
                {...row.getRowProps()}
                className={
                  isEven(idx)
                    ? "bg-slate-300 hover:bg-slate-400"
                    : "bg-slate-100 hover:bg-slate-200"
                }
                key={idx}
              >
                {row.cells.map((cell, idx) => {
                  return (
                    <td {...cell.getCellProps()} key={idx}>
                      {cell.render("Cell")}
                    </td>
                  );
                })}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
};

export default LiftsTable;
