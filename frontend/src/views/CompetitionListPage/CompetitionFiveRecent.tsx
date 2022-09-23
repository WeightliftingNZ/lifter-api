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
      <Box sx={{ mt: 2 }}>
        {isLoading && <CustomLoading />}
        {isError && <CustomError />}
        {isSuccess && (
          <>
            <Stack sx={{ maxWidth: "max-content" }} spacing={1}>
              {data?.results.map((competition: CompetitionListObjectProps) => (
                <>
                  <CompetitionCard
                    key={competition.reference_id}
                    referenceId={competition.reference_id}
                    name={competition.name}
                    liftCount={competition.lifts_count}
                    dateStart={competition.date_start}
                    dateEnd={competition.date_end}
                    randomLifts={competition.random_lifts}
                  />
                  {console.dir(competition)}
                </>
              ))}
            </Stack>
          </>
        )}
      </Box>
    </>
  );
};

export default CompetitionFiveRecent;
