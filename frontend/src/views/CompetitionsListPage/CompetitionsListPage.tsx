import React, { useState } from "react";
import { useQuery } from "react-query";
import { Link } from "react-router-dom";
import apiClient from "../../utils/http-common";
import { CompetitionObject } from "../../interfaces";

const CompetitionsListPage = () => {
  const [competitions, setCompetitions] = useState({
    count: 0,
    next: "",
    previous: "",
    results: [],
  });

  const { isLoading, isError } = useQuery(
    "competitions",
    async () => {
      return await apiClient.get("/competitions");
    },
    {
      enabled: Boolean(competitions),
      onSuccess: (res) => {
        const result = {
          status: res.status + "-" + res.statusText,
          headers: res.headers,
          data: res.data,
        };
        setCompetitions(result.data);
      },
      onError: (err) => {
        console.log(err);
      },
    }
  );
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
      {competitions.results.map((competition: CompetitionObject, idx) => (
        <Link
          key={idx}
          className="card"
          to={`/competitions/${competition.reference_id}`}
        >
          <h1>{competition.competition_name}</h1>
          <p>{competition.location}</p>
          <p>{competition.date_start}</p>
          <p>Sessions: {competition.session_count}</p>
          <p>Athletes: {competition.lift_count}</p>
        </Link>
      ))}
    </>
  );
};

export default CompetitionsListPage;
