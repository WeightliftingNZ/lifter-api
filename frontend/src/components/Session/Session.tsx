import React from "react";
import { useQuery } from "react-query";
import apiClient from "../../utils/http-common";
import sessionDateTimeConvert from "../../utils/time-converter";
import LiftsTable from "../LiftsTable";
import Loading from "../Loading";
import Error from "../Error";

const Session = ({ sessionId, competitionId }: any) => {
  if (!sessionId) {
    return (
      <>
        <div>Please select a session.</div>
      </>
    );
  }
  const { data, error, isLoading, isError } = useQuery(
    ["session", sessionId],
    async () => {
      return await apiClient.get(
        `/competitions/${competitionId}/sessions/${sessionId}`
      );
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
    console.log(error);
    return (
      <>
        <Error />
      </>
    );
  }
  const session = data?.data;
  const lifts = session.lift_set;
  return (
    <>
      <div className="mt-6 card self-center">
        <div>
          <h1>Session: {session.session_number}</h1>
          <p>
            {sessionDateTimeConvert(
              session.session_datetime || "1900-01-01T00:00+13:00"
            )}
          </p>
        </div>
        <div className="flex flex-col justify-center">
          <div>
            <b>Referees:</b>
          </div>
          <div className="flex justify-around gap-5">
            <div>
              <b>1st:</b> {session.referee_first}
            </div>
            <div>
              <b>2nd:</b> {session.referee_second}
            </div>
            <div>
              <b>3rd:</b> {session.referee_third}
            </div>
          </div>
        </div>
        <div className="flex flex-col">
          <div className="flex flex-col">
            <b>Jury:</b> <div className="pl-1">{session.jury}</div>
          </div>
          <div>
            <b>Technical Controller:</b> {session.technical_controller}
          </div>
          <div>
            <b>Marshall:</b> {session.marshall}
          </div>
          <div>
            <b>Announcer:</b> {session.announcer}
          </div>
          <div>
            <b>Timekeeper:</b> {session.timekeeper}
          </div>
        </div>
      </div>
      <div>
        <LiftsTable lifts={lifts} />
      </div>
    </>
  );
};

export default Session;
