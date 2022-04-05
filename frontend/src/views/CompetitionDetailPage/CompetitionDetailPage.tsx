import React, { useState, FunctionComponent } from "react";
import { useQuery } from "react-query";
import { useParams, Link } from "react-router-dom";
import apiClient from "../../utils/http-common";
import Loading from "../../components/Loading";
import Error from "../../components/Error";
import LiftsTable from "../../components/LiftsTable";

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
      },
    ],
  });
  const params = useParams();
  const competitionId = params.competitionReferenceId;
  const sessionId = params.sessionReferenceId;

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

  // sessions from a competition
  const sessions = competition.session_set;

  const Session = ({ sessions, sessionId, competitionId }: any) => {
    if (competition.session_set.length === 0) {
      return (
        <>
          <div>{competition.competition_name} Competition has no sessions!</div>
        </>
      );
    }
    if (!sessionId) {
      return <div>Please select a session</div>;
    }
    return (
      <>
        <div className="mt-6 card">
          <div className="flex justify-around gap-5">
            <div>First Referee: {sessions[selectedSession].referee_first}</div>
            <div>
              Second Referee: {sessions[selectedSession].referee_second}
            </div>
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
        <div>
          <LiftsTable competitionId={competitionId} sessionId={sessionId} />
        </div>
      </>
    );
  };

  // const lifts = competition.session_set[selectedSession].lift_set;
  // add another session

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
      <div className="flex gap-2">
        {sessions.map((session, idx) => {
          return (
            <Link
              key={idx}
              to={`/competitions/${competitionId}/sessions/${session.reference_id}`}
            >
              <button
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
            </Link>
          );
        })}
      </div>
      <div className="flex flex-col">
        <Session
          sessions={sessions}
          sessionId={sessionId}
          competitionId={competitionId}
        />
      </div>
    </>
  );
};

export default CompetitionDetailPage;
