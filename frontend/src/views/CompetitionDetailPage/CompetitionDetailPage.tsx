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
import CompetitionDetailLoading from "./CompetitionDetailLoading";
import moment from "moment";

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
        flexWrap: "wrap",
        gap: 2,
        justifyContent: "flex-start",
      }}
    >
      {isLoading && !data && <CompetitionDetailLoading />}
      {isError && <CustomError />}
      {isSuccess && data && (
        <>
          <Box sx={{ m: 1 }}>
            <Title>{data?.name}</Title>
            <Box sx={{ display: "flex", gap: 2 }}>
              {data?.location}
              <br />
              {dateRangeProvider(data?.date_start, data?.date_end)}
              <br />
              Athletes: {data?.lifts_count}
            </Box>
          </Box>
          <LiftTable liftSet={data?.lift_set} />
          <Box sx={{ m: 1 }}>
            {`Last Updated: ${moment(data?.last_edited).format(
              "dddd, MMMM Do YYYY, h:mm a"
            )}`}
          </Box>
        </>
      )}
    </Box>
  );
};

export default CompetitionDetailPage;
