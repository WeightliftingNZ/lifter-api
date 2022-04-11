import React, { useState } from "react";
import { useQuery } from "react-query";
import apiClient from "../../utils/http-common";
import LiftsTable from "../LiftsTable";
import Loading from "../Loading";
import Error from "../Error";

function timeConvert(hours: number, minutes: number) {
  // hours and minutes in 24 hours time
  if (!(hours >= 0 && hours <= 23)) {
    throw new RangeError("Hours must between 0 and 23");
  }
  if (!(minutes >= 0 && minutes <= 59)) {
    throw new RangeError("Minutes must between 0 and 59");
  }

  let newHours: number = hours;
  let newMinutes: string = String(minutes);
  let format: string = "AM";

  if (hours === 0) {
    newHours = 12;
    format = "AM";
  }
  if (hours > 12) {
    newHours = hours - 12;
    format = "PM";
  }
  if (String(minutes).length === 1) {
    newMinutes = "0" + String(minutes);
  }

  return `${newHours}:${newMinutes} ${format}`;
}

function sessionDateTimeConvert(s: string) {
  // convert ISO datetime string into human readable date and time
  const date = new Date(s);
  const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  return `${days[date.getDay()]}, ${date.getDate()} ${
    months[date.getMonth()]
  } ${date.getFullYear()} - ${timeConvert(date.getHours(), date.getMinutes())}`;
}

const Session = ({ sessionId, competitionId }: any) => {
  const [session, setSession] = useState({
    reference_id: "",
    session_number: "",
    session_datetime: "",
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
        <div>
          <h1>Session: {session.session_number}</h1>
          {console.log(new Date(session.session_datetime))}
          <p>{sessionDateTimeConvert(session.session_datetime)}</p>
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
