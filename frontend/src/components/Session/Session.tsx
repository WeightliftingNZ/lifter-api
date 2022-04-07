import React, { useState } from "react";
import { useQuery } from "react-query";
import apiClient from "../../utils/http-common";
import LiftsTable from "../LiftsTable";
import Loading from "../Loading";
import Error from "../Error";

const Session = ({ sessionId, competitionId }: any) => {
  const [session, setSession] = useState({
    reference_id: "",
    referee_first: "",
    referee_second: "",
    referee_third: "",
    jury: "",
    marshall: "",
    technical_controller: "",
    timekeeper: "",
    announcer: "",
    lift_set: [{ weight_category: "" }],
  });
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
        console.log("sessionId: ", sessionId);
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
  const lifts = session.lift_set;
  return (
    <>
      <div className="mt-6 card self-center">
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
