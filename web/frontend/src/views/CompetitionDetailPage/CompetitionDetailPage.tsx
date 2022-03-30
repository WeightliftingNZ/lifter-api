import React, {
  useState,
  useMemo,
  FunctionComponent,
  PropsWithChildren,
} from "react";
import { useQuery } from "react-query";
import { useTable } from "react-table";
import { Link, useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import Loading from "../../components/Loading";
import Error from "../../components/Error";

const Table = ({ lifts }: any) => {
  const isEven = (idx: number) => idx % 2 !== 0;

  const displayWeightCell = ({ cell }: { cell: any }) => {
    let bolded = false;
    let arrayLiftType = cell.column.id.split(".");
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
  console.dir(lifts);

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

  return (
    <div className="flex self-center">
      <table {...getTableProps}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>{column.render("Header")}</th>
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
                    <td {...cell.getCellProps()}>{cell.render("Cell")}</td>
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

const CompetitionDetailPage: FunctionComponent = () => {
  const [selectedSession, setSelectedSession] = useState(0);
  const [competition, setCompetition] = useState({
    url: "",
    reference_id: "",
    date_start: "",
    date_end: "",
    location: "",
    competition_name: "",
    session_count: 0,
    session_set: [
      {
        reference_id: "",
        session_number: "",
        session_datetime: "",
        competition: "",
        competition_name: "",
        referee_first: "",
        referee_second: "",
        referee_third: "",
        technical_controller: "",
        marshall: "",
        timekeeper: "",
        jury: "",
        lift_count: "",
        lift_set: [],
      },
    ],
  });
  const params = useParams();
  const competitionId = params.competitionReferenceId;

  const { isLoading, isError } = useQuery(
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
        console.log(err);
      },
    }
  );

  const sessions = competition.session_set;

  if (competition.session_set.length === 0) {
    return (
      <>
        <div>This Competition has no Sessions!!</div>
      </>
    );
  }

  const lifts = competition.session_set[selectedSession].lift_set;

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
  return (
    <>
      <div className="card">
        <h1>{competition.competition_name}</h1>
        {competition.location}
      </div>
      <div className="mt-6 card">
        <div className="flex justify-around gap-5">
          <div>First Referee: {sessions[selectedSession].referee_first}</div>
          <div>Second Referee: {sessions[selectedSession].referee_second}</div>
          <div>Third Referee: {sessions[selectedSession].referee_third}</div>
        </div>
        <div className="flex justify-start gap-5">
          <div>
            Technical Controller:{" "}
            {sessions[selectedSession].technical_controller}
          </div>
          <div>Marshall: {sessions[selectedSession].marshall}</div>
        </div>
        <div className="flex justify-start gap-5">
          <div>Timekeeper: {sessions[selectedSession].timekeeper}</div>
          <div>Jury: {sessions[selectedSession].jury}</div>
        </div>
      </div>
      <div className="flex gap-2">
        {sessions.map((session, idx) => {
          return (
            <button
              key={idx}
              onClick={() => {
                setSelectedSession(Number(session.session_number) - 1);
              }}
              className={
                Number(session.session_number) === selectedSession + 1
                  ? "btn bg-slate-600 border-blue-300"
                  : "btn"
              }
            >
              {session.session_number}
            </button>
          );
        })}
      </div>
      <div>
        {console.dir(lifts)}
        <Table lifts={lifts} />
      </div>
    </>
  );
};

export default CompetitionDetailPage;
