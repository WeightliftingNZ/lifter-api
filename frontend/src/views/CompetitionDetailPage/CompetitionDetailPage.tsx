/** @format */

import React from "react";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import CustomError from "../../components/Error";
import Box from "@mui/material/Box";
import Title from "../../components/Title";
import { dateRangeProvider } from "../../utils/customFunctions/customFunctions";
import LiftTable from "./LiftTable";
import CustomLoading from "./Loading";
import moment from "moment";
import { Alert } from "@mui/material";
import SubTitle from "../../components/SubTitle";
import CompetitionBadges from "../../components/CompetitionBadges";

const CompetitionDetailPage: React.FC = () => {
  const params = useParams();
  const competitionId = params.competitionReferenceId;

  const fetchCompetition = async () => {
    const res = await apiClient.get(`/competitions/${competitionId}`);
    return res.data;
  };

  const { data, isLoading, isError, isSuccess, error } = useQuery(
    ["competitions", competitionId],
    () => fetchCompetition(),
    { enabled: true }
  );

  if (isError) {
    console.log(error);
  }

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      {isLoading && !data && <CustomLoading />}
      {isError && <CustomError />}
      {isSuccess && data && (
        <>
          <Box sx={{ m: 1 }}>
            <Title>{data?.name}</Title>
            <CompetitionBadges name={data?.name} />
            <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
              <Box>{data?.location}</Box>
              <Box>{dateRangeProvider(data?.date_start, data?.date_end)}</Box>
              {data?.lifts_count > 1 && (
                <Box>Athletes: {data?.lifts_count}</Box>
              )}
            </Box>
          </Box>
          {data?.lift_count === 0 ? (
            <Alert severity="info">Pending results</Alert>
          ) : (
            <LiftTable liftSet={data?.lift_set} />
          )}
          <Box sx={{ m: 1 }}>
            Last Updated:
            <SubTitle>
              {`Competition details: ${moment(
                data?.competition_last_edited
              ).format("dddd, MMMM Do YYYY, h:mm a")}`}
            </SubTitle>
            <SubTitle>
              {`Lift details: ${moment(data?.lift_last_edited).format(
                "dddd, MMMM Do YYYY, h:mm a"
              )}`}
            </SubTitle>
          </Box>
        </>
      )}
    </Box>
  );
};

export default CompetitionDetailPage;
