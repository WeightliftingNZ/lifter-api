import React, { useState, useMemo, FunctionComponent } from "react";
import { useQuery } from "react-query";
import { useTable } from "react-table";
import { Link, useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";

const CompetitionDetailPage: FunctionComponent = () => {
  const [competition, setCompetition] = useState({
    url: "",
    reference_id: "",
    date_start: "",
    date_end: "",
    location: "",
    competition_name: "",
    lift_count: 0,
    lift_set: [],
  });
  let params = useParams();
  const competitionId = params.competitionReferenceId;

  const { isLoading, isSuccess, isError, error, refetch } = useQuery(
    ["competition", competitionId],
    async () => {
      return await apiClient.get(`/competitions/${competitionId}`);
    },
    {
      enabled: Boolean(competition),
      onSuccess: (res) => {
        const result = {
          status: res.status + "-" + res.statusText,
          headers: res.headers,
          data: res.data,
        };
        setCompetition(result.data);
      },
      onError: (err) => {
        console.log("Error");
      },
    }
  );

  // learn react-table
  const isEven = (idx: number) => idx % 2 !== 0;

  const lifts = competition.lift_set;

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
        Header: "Cat.",
        accessor: "weight_category",
      },
      {
        Header: "Team",
        accessor: "team",
      },
      {
        Header: "Snatch",
        columns: [
          {
            Header: "1",
            accessor: "snatches.1st",
            Cell: ({ cell }: { cell: any }) => {
              return <h1>{cell.value}</h1>;
            },
          },
          {
            Header: "2",
            accessor: "snatches.2nd",
          },
          {
            Header: "3",
            accessor: "snatches.3rd",
          },
        ],
      },
      {
        Header: "Clean & Jerk",
        columns: [
          {
            Header: "1",
            accessor: "cnjs.1st",
          },
          {
            Header: "2",
            accessor: "cnjs.2nd",
          },
          {
            Header: "3",
            accessor: "cnjs.3rd",
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
    return (
      <>
        <p>Loading...</p>
      </>
    );
  }
  if (isError) {
    return (
      <>
        <p>Error!!</p>
      </>
    );
  }
  return (
    <>
      <div className="card">
        <h1>{competition.competition_name}</h1>
        {competition.location}
      </div>
      <div className="container">
        <table {...getTableProps}>
          <thead>
            {headerGroups.map((headerGroup) => (
              <tr {...headerGroup.getHeaderGroupProps()}>
                {headerGroup.headers.map((column) => (
                  <th {...column.getHeaderProps()}>
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
                >
                  {row.cells.map((cell) => {
                    return (
                      <td
                        {...cell.getCellProps()}
                        className={
                          cell.value.lift_status == "LIFT"
                            ? ""
                            : cell.value.lift_status == "NOLIFT"
                            ? "line-through"
                            : ""
                        }
                      >
                        {cell.column.parent
                          ? cell.column.parent.Header == "Snatch" ||
                            cell.column.parent.Header == "Clean & Jerk"
                            ? cell.value.lift_status == "DNA"
                              ? "-"
                              : cell.value.weight
                            : cell.render("Cell")
                          : cell.render("Cell")}
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

export default CompetitionDetailPage;
