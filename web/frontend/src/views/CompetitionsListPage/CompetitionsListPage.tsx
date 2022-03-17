import React, { useState, useEffect } from "react";
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import { CompetitionObject } from "../../interfaces";

const CompetitionsListPage = () => {
  const [competitions, setCompetitions] = useState({
    count: 0,
    next: "",
    previous: "",
    results: [],
  });
  const [search, setSearch] = useState("");

  const { isLoading, isSuccess, isError, data, error, refetch } = useQuery(
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
        console.log("Error: " + error);
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
      {competitions.results.map((competition: CompetitionObject) => (
        <Link
          key={competition.reference_id}
          className="card"
          to={`/competitions/${competition.reference_id}`}
        >
          <h1>{competition.competition_name}</h1>
          <span>
            {competition.location} - {competition.lift_count}
          </span>
        </Link>
      ))}
    </>
  );
};

export default CompetitionsListPage;
