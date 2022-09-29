/** @format */

import React, { useState } from "react";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import CustomLoading from "../../components/Loading";
import CustomError from "../../components/Error";
import CustomTable from "./table";
import {
  AgeCategoriesProps,
  AthleteDetailObjectProps,
  LiftObjectProps,
} from "../../interfaces";
import Alert from "@mui/material/Alert";
import Card from "@mui/material/Card";
import Box from "@mui/material/Box";
import { Column } from "./interfaces";
import Paper from "@mui/material/Paper";
import Title from "../../components/Title";
import AgeCategoryBadges from "../../components/AgeCategoryBadges";
import moment from "moment";

import {
  ResponsiveContainer,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";
import { CardContent, Typography, Stack, Tabs, Tab } from "@mui/material";
import { useTheme } from "@mui/material/styles";

interface LiftChartDataProps {
  name: string;
  snatch: number;
  cnj: number;
  total: number;
  date: string;
}

interface LiftChartProps {
  data: LiftChartDataProps[];
}

/* TODO: types? */
const CustomTooltip = (props: any) => {
  const { active, payload } = props;
  if (active) {
    return (
      <>
        <Card>
          <CardContent>
            <Stack spacing={1}>
              {payload.map((item: any) => {
                let value = item.value;
                if (item.name === "Date") {
                  value = moment(item.value, "X").format("YYYY-MM-DD");
                }
                return (
                  <Typography variant="body1" key={item.name}>
                    {item.name}: {value}
                  </Typography>
                );
              })}
            </Stack>
          </CardContent>
        </Card>
      </>
    );
  }
};

const LiftChart: React.FC<LiftChartProps> = (props: LiftChartProps) => {
  const { data } = props;
  const theme = useTheme();

  return (
    <Paper>
      <Box sx={{ mx: 2, my: 4 }}>
        <Title>Lifts</Title>
        <ResponsiveContainer width="75%" height={500}>
          <ScatterChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="date"
              domain={["dataMin", "dataMax"]}
              name="Date"
              tickFormatter={(unixTime) =>
                moment(unixTime, "X").format("YYYY-MM-DD")
              }
              type="number"
            ></XAxis>
            <YAxis name="Weight" unit="kg"></YAxis>
            <Scatter
              dataKey="total"
              line
              fill={theme.palette.primary.main}
              lineJointType="monotone"
              lineType="joint"
              name="Total"
            />
            <Scatter
              dataKey="snatch"
              line
              fill={theme.palette.secondary.light}
              lineJointType="monotone"
              lineType="joint"
              name="Snatch"
            />
            <Scatter
              dataKey="cnj"
              fill={theme.palette.secondary.main}
              line
              lineJointType="monotone"
              lineType="joint"
              name="Clean and Jerk"
            />
            <Tooltip content={CustomTooltip} />
            <Legend />
          </ScatterChart>
        </ResponsiveContainer>
      </Box>
    </Paper>
  );
};

const columns: Column[] = [
  { id: "placing", label: "Placing" },
  { id: "competition_name", label: "Competition" },
  { id: "competition_date_start", label: "Date" },
  { id: "weight_category", label: "Cat." },
  { id: "bodyweight", label: "Weight" },
  { id: "team", label: "Team" },
  { id: "snatch_first_weight", label: "1", align: "center" },
  { id: "snatch_second_weight", label: "2", align: "center" },
  { id: "snatch_third_weight", label: "3", align: "center" },
  { id: "cnj_first_weight", label: "1", align: "center" },
  { id: "cnj_second_weight", label: "2", align: "center" },
  { id: "cnj_third_weight", label: "3", align: "center" },
  {
    id: "total_lifted",
    label: "Total",
    align: "center",
    extra: { fontWeight: "bold" },
  },
  {
    id: "sinclair",
    label: "Sinclair",
    align: "center",
    extra: { fontWeight: "bold" },
  },
];

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
  const fullName: string = parsedData.full_name;
  const liftsCount: number = parsedData.lift_set.length;
  const ageCategories: AgeCategoriesProps = parsedData.age_categories;

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
        flexWrap: "wrap",
        flexDirection: "column",
        gap: 2,
      }}
    >
      {isLoading && !data && <CustomLoading />}
      {isError && <CustomError />}
      {isSuccess && data && (
        <>
          <Title>{fullName}</Title>
          <AgeCategoryBadges ageCategories={ageCategories} />
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
            <Alert severity="info">No lifts recorded for "{fullName}"</Alert>
          ) : (
            <>
              {value === 0 && (
                <Box>
                  <CustomTable rows={rows} columns={columns} />
                </Box>
              )}
              {value === 1 && (
                <Box>
                  <LiftChart data={chartData} />
                </Box>
              )}
            </>
          )}
        </>
      )}
    </Box>
  );
};

export default AthleteDetailPage;
