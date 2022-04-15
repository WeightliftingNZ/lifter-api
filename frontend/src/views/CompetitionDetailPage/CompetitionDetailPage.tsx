import React, { useState, FunctionComponent } from "react";
import { useQuery } from "react-query";
import { useParams, Link } from "react-router-dom";
import apiClient from "../../utils/http-common";
import Loading from "../../components/Loading";
import Error from "../../components/Error";
import Session from "../../components/Session";

const CompetitionDetailPage: FunctionComponent = () => {
  const [selectedSession, setSelectedSession] = useState("");

  const params = useParams();
  const competitionId = params.competitionReferenceId;
  const sessionId = params.sessionReferenceId;

  const { data, isLoading, isError } = useQuery(
    ["competition", competitionId],
    async () => {
      return await apiClient.get(`/competitions/${competitionId}`);
    }
  );

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

  const competition: any = data?.data;

  // sessions from a competition
  const sessions = competition.session_set.reduce(
    (obj: any, item: any) => Object.assign(obj, { [item.reference_id]: item }),
    {}
  );

  return (
    <>
      <div className="card">
        <h1>{competition.competition_name}</h1>
        <p>{competition.location}</p>
        <p>{competition.date_start}</p>
      </div>
      <div className="flex gap-2">
        {Object.keys(sessions).map((newSessionId, idx) => {
          return (
            <Link
              key={idx}
              to={`/competitions/${competitionId}/sessions/${newSessionId}`}
            >
              <button
                onClick={() => {
                  setSelectedSession(newSessionId);
                }}
                className={
                  newSessionId === selectedSession
                    ? "btn bg-slate-600 border-blue-300"
                    : "btn"
                }
              >
                {idx}
              </button>
            </Link>
          );
        })}
      </div>
      <div className="flex flex-col gap-2">
        {competition.session_set.length === 0 ? (
          <div className="error-msg">This competition has no sessions!</div>
        ) : (
          <Session
            sessionId={selectedSession || sessionId}
            competitionId={competitionId}
          />
        )}
      </div>
    </>
  );
};

export default CompetitionDetailPage;
