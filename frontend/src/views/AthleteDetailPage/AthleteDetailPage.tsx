/** @format */

import React, { useState } from "react";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import CustomLoading from "../../components/Loading";
import CustomError from "../../components/Error";
import Box from "@mui/material/Box";
import Title from "../../components/Title";
import AgeCategoryBadges from "../../components/AgeCategoryBadges";
import { Tabs, Tab } from "@mui/material";
import GradeBadges from "../../components/GradeBadges";
import LiftTable from "./LiftTable";
import NoResults from "../../components/NoResults";
import LastUpdated from "../../components/LastUpdated";
import StatsTab from "./StatsTab";

const AthleteDetailPage: React.FC = () => {
  const params = useParams();
  const AthleteId = params.athleteReferenceId;
  const [tabValue, setTabValue] = useState(params["*"] === "stats" ? 1 : 0);

  const handleOnChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const fetchAthlete = async () => {
    const res = await apiClient.get(`/athletes/${AthleteId}`);
    return res.data;
  };

  const { data, error, isLoading, isError, isSuccess } = useQuery(
    ["athlete", AthleteId],
    () => fetchAthlete(),
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
        p: 1,
      }}
    >
      {isLoading && !data && <CustomLoading />}
      {isError && <CustomError />}
      {isSuccess && data && (
        <>
          <Title>{data?.full_name}</Title>
          <GradeBadges grade={data?.current_grade} />
          <AgeCategoryBadges ageCategories={data?.age_categories} />
          <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
            {data?.lifts_count > 1 && (
              <Box>
                <b>{data?.lifts_count}</b> Competitions
              </Box>
            )}
          </Box>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <Tabs
              value={tabValue}
              onChange={handleOnChange}
              aria-label="athlete selection tabs"
            >
              <Tab label="Lifts"></Tab>
              <Tab label="Stats"></Tab>
            </Tabs>
          </Box>
          {data?.lift_set.length === 0 ? (
            <NoResults />
          ) : (
            <>
              {tabValue === 0 && (
                <Box>
                  <LiftTable liftSet={data?.lift_set} />
                </Box>
              )}
              {tabValue === 1 && (
                <Box>
                  <StatsTab athlete={data} />
                </Box>
              )}
            </>
          )}

          <LastUpdated
            update={[data?.athlete_last_edited, data?.lift_last_edited]}
          />
        </>
      )}
    </Box>
  );
};

export default AthleteDetailPage;
