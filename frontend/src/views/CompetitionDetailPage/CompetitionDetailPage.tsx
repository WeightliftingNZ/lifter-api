import React, { FunctionComponent } from "react";
import { useParams } from "react-router-dom";
import { styled } from "@mui/material/styles";

const CompetitionDetailPage: FunctionComponent = () => {
  const params = useParams();
  const competitionId = params.competitionReferenceId;
  return (
    <>
      <p>{competitionId}</p>
    </>
  );
};

export default CompetitionDetailPage;
