/** @format */

import React, { useState } from "react";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import CustomLoading from "../../components/Loading";
import CustomError from "../../components/Error";
import { AthleteDetailObjectProps, LiftObjectProps } from "../../interfaces";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Title from "../../components/Title";
import AgeCategoryBadges from "../../components/AgeCategoryBadges";
import moment from "moment";
import { Tabs, Tab } from "@mui/material";
import { LiftChartDataProps } from "./SinclairChart/interfaces";
import SinclairChart from "./SinclairChart";
import GradeBadges from "../../components/GradeBadges";
import LiftTable from "./LiftTable";
import SubTitle from "../../components/SubTitle";

const AthleteDetailPage: React.FC = () => {
  const params = useParams();
  const AthleteId = params.athleteReferenceId;
  const [value, setValue] = useState(0);

  const handleOnChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
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

  if (isLoading) {
    return <CustomLoading />;
  }

  if (isError) {
    console.log(error);
  }

  const parsedData: AthleteDetailObjectProps = data;
  const rows: LiftObjectProps[] = parsedData.lift_set;
  const liftsCount: number = parsedData.lift_set.length;

  const chartData: LiftChartDataProps[] = [];

  rows.map((row) => {
    const chartDatum: LiftChartDataProps = {
      name: row.competition_name,
      snatch: row.best_snatch_weight[1],
      cnj: row.best_cnj_weight[1],
      total: row.total_lifted,
      date: moment(row.competition_date_start, "YYYY-MM-DD").format("X"),
    };
    chartData.push(chartDatum);
    return null;
  });

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
          <Title>{data?.full_name}</Title>
          <GradeBadges grade={data?.current_grade} />
          <AgeCategoryBadges ageCategories={data?.age_categories} />
          <Box sx={{ display: "flex", flexDirection: "column", gap: 1 }}>
            {data?.lifts_count > 1 && (
              <Box>Number time competed: {data?.lifts_count}</Box>
            )}
          </Box>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <Tabs
              value={value}
              onChange={handleOnChange}
              aria-label="athlete selection tabs"
            >
              <Tab label="Lifts"></Tab>
              <Tab label="Stats"></Tab>
            </Tabs>
          </Box>
          {liftsCount === 0 ? (
            <Alert severity="info">No results available</Alert>
          ) : (
            <>
              {value === 0 && (
                <Box>
                  <LiftTable liftSet={data?.lift_set} />
                </Box>
              )}
              {value === 1 && (
                <Box>
                  <SinclairChart data={chartData} />
                </Box>
              )}
            </>
          )}

          <Box sx={{ m: 1 }}>
            Last Updated:
            <SubTitle>
              {`Athlete details: ${moment(data?.athlete_last_edited).format(
                "dddd, MMMM Do YYYY, h:mm a"
              )}`}
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

export default AthleteDetailPage;
