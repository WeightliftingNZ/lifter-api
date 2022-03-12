import React, { useState, useEffect } from "react";
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";

interface CompetitionObject {
  reference_id: string;
  url: string;
  competition_name: string;
  location: string;
  date_end?: string;
  date_start?: string;
}

const CompetitionsListPage = () => {
  const [competitions, setCompetitions] = useState([]);

  const { isLoading, isError, data, error, refetch } = useQuery(
    "competitions",
    async () => {
      return await apiClient.get("/competitions");
    },
    {
      enabled: true,
      retry: 2,
      onSuccess: (res) => {
        const result = {
          status: res.status + "-" + res.statusText,
          headers: res.headers,
          data: res.data,
        };
        setCompetitions(result.data);
      },
      onError: (err) => {
        console.log("Error");
      },
    }
  );

  return (
    <>
      {competitions.map((competition: CompetitionObject) => (
        <Link
          key={competition.reference_id}
          className="card"
          to={`/competitions/${competition.reference_id}`}
        >
          <h1>{competition.competition_name}</h1>
          <span>{competition.location}</span>
        </Link>
      ))}
    </>
  );
};

export default CompetitionsListPage;
