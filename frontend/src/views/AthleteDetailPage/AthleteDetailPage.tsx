import React, { useState, FunctionComponent, useMemo } from "react";
import { useQuery } from "react-query";
import { useTable } from "react-table";
import { Link, useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import Loading from "../../components/Loading";
import Error from "../../components/Error";

const AthleteDetailPage: FunctionComponent = () => {
  const [athlete, setAthlete] = useState({
    first_name: "",
    last_name: "",
    full_name: "",
    yearborn: 1900,
    lift_set: [],
  });
  const params = useParams();
  const athleteId = params.athleteReferenceId;

  const { isLoading, isError } = useQuery(
    ["athlete", athleteId],
    async () => {
      return await apiClient.get(`/athletes/${athleteId}`);
    },
    {
      enabled: Boolean(athlete),
      onSuccess: (res) => {
        const result = {
          status: res.status + "-" + res.statusText,
          headers: res.headers,
          data: res.data,
        };
        setAthlete(result.data);
      },
      onError: (err) => {
        console.log(err);
      },
    }
  );

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

  const lifts = athlete.lift_set;

  const liftData = useMemo(() => [...lifts], [lifts]);

  const liftColumns = useMemo(
    () => [
      {
        Header: "Competition",
        accessor: "competition_name",
        Cell: ({ cell }: { cell: any }) => {
          return (
            <Link
              to={`/competitions/${cell.row.original.competition}/sessions/${cell.row.original.session}`}
            >
              <div className="text-left text-blue-600 font-semibold underline">
                {cell.value}
              </div>
            </Link>
          );
        },
      },
      {
        Header: "Date",
        accessor: "competition_date_start",
      },
      {
        Header: "Cat.",
        accessor: "weight_category",
      },
      {
        Header: "Weight",
        accessor: "bodyweight",
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
    return <Loading />;
  }
  if (isError) {
    return <Error />;
  }

  return (
    <>
      <div className="card">
        <h1>
          {athlete.first_name} {athlete.last_name.toUpperCase()}
        </h1>
        {athlete.yearborn}
      </div>
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
                <tr {...row.getRowProps()} key={idx}>
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
    </>
  );
};

export default AthleteDetailPage;
