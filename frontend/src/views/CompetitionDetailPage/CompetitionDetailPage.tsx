import React, { FunctionComponent } from "react";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import Loading from "../../components/Loading";
import Error from "../../components/Error";
import LiftsTable from "../../components/LiftsTable";

const CompetitionDetailPage: FunctionComponent = () => {
  const params = useParams();
  const competitionId = params.competitionReferenceId;

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
  const lifts = competition.lift_set;

  return (
    <>
      <div className="card">
        <h1>{competition.name}</h1>
        <p>{competition.location}</p>
        <p>{competition.date_start}</p>
      </div>
      <div className="flex flex-col gap-2">
        {competition.lift_set.length === 0 ? (
          <div className="error-msg">This competition has no lifts!</div>
        ) : (
          <LiftsTable lifts={lifts} />
        )}
      </div>
    </>
  );
};

export default CompetitionDetailPage;
