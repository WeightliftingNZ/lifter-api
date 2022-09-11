import React from "react";
import { useParams } from "react-router-dom";

const CompetitionDetailPage: React.FC = () => {
  const params = useParams();
  const competitionId = params.competitionReferenceId;
  return (
    <>
      <h1>{competitionId}</h1>
    </>
  );
};

export default CompetitionDetailPage;
