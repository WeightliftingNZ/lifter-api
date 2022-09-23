import { Box, Stack } from "@mui/system";
import { useQuery } from "react-query";
import React from "react";
import apiClient from "../../utils/http-common/http-common";
import { CompetitionListObjectProps } from "../../interfaces";
import CustomError from "../../components/Loading";
import CustomLoading from "../../components/Error";
import CompetitionCard from "./CompetitionCard";

const CompetitionFiveRecent: React.FC = () => {
  const fetchFiveRecentCompetitions = async () => {
    const PAGE_LIMIT = 5;
    const res = await apiClient.get(`/competitions?page_size=${PAGE_LIMIT}`);
    return res.data;
  };

  const { data, error, isLoading, isError, isSuccess } = useQuery(
    ["competitionsHomePage"],
    () => fetchFiveRecentCompetitions()
  );

  if (isError) {
    console.log(error);
  }

  if (!data) {
    return null;
  }

  return (
    <>
      {isLoading && <CustomLoading />}
      {isError && <CustomError />}
      {isSuccess && (
        <Box
          sx={{
            display: "flex",
            flex: 1,
            gap: 2,
            justifyContent: "flex-start",
            flexWrap: "wrap",
            alignItems: "stretch",
          }}
        >
          {data?.results.map((competition: CompetitionListObjectProps) => (
            <Box sx={{ flexGrow: 0, flexShrink: 0, flexBasis: "31%" }}>
              <CompetitionCard
                key={competition.reference_id}
                referenceId={competition.reference_id}
                name={competition.name}
                liftCount={competition.lifts_count}
                dateStart={competition.date_start}
                dateEnd={competition.date_end}
                randomLifts={competition.random_lifts}
              />
            </Box>
          ))}
        </Box>
      )}
    </>
  );
};

export default CompetitionFiveRecent;
