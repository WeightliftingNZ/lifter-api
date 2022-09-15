import React from "react";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import CustomLoading from "../../components/Loading";
import CustomError from "../../components/Error";
import CustomTable from "./table";
import { AthleteDetailObjectProps, LiftObjectProps } from "../../interfaces";
import Alert from "@mui/material/Alert";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { Column } from "./interfaces";
import Paper from "@mui/material/Paper";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

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

const LiftChart: React.FC<LiftChartProps> = (props: LiftChartProps) => {
  const { data } = props;
  return (
    <Paper>
      <Box sx={{ mx: 2 }}>
        <Typography variant="h6" gutterBottom>
          Lifts
        </Typography>
        <LineChart width={600} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="competition_date_start" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="snatch" stroke="#00AA00" />
          <Line type="monotone" dataKey="cnj" stroke="#AA0000" />
          <Line type="monotone" dataKey="total" stroke="#0000AA" />
        </LineChart>
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
  { id: "cnj_second_weight", label: "1", align: "center" },
  { id: "cnj_first_weight", label: "2", align: "center" },
  { id: "cnj_third_weight", label: "3", align: "center" },
  {
    id: "total_lifted",
    label: "Total",
    align: "center",
    extra: { fontWeight: "bold" },
  },
];

const AthleteDetailPage: React.FC = () => {
  const params = useParams();
  const AthleteId = params.athleteReferenceId;

  const { data, isLoading, isError } = useQuery(
    ["athlete", AthleteId],
    async () => {
      const res = await apiClient.get(`/athletes/${AthleteId}`);
      return res.data;
    }
  );
  if (isLoading) {
    return <CustomLoading />;
  }

  if (isError) {
    return <CustomError />;
  }

  const parsedData: AthleteDetailObjectProps = data;
  const rows: LiftObjectProps[] = parsedData.lift_set;
  const fullName: string = parsedData.full_name;
  const birthYear: number = parsedData.yearborn;
  const liftsCount: number = parsedData.lift_set.length;

  const chartData: LiftChartDataProps[] = [];

  rows.map((row) => {
    const chartDatum: LiftChartDataProps = {
      name: row.competition_name,
      snatch: row.best_snatch_weight[1],
      cnj: row.best_cnj_weight[1],
      total: row.total_lifted,
      date: row.competition_date_start,
    };
    chartData.push(chartDatum);
    return null;
  });

  return (
    <>
      <Box>
        <Typography variant="h4" gutterBottom>
          {fullName}
        </Typography>
        <Typography variant="subtitle2">{birthYear}</Typography>
      </Box>
      <Box sx={{ mt: 6 }}>
        {liftsCount === 0 ? (
          <Alert severity="info">
            No lifts recorded for "{fullName}" competition
          </Alert>
        ) : (
          <>
            <Box>
              <LiftChart data={chartData} />
            </Box>
            <Box>
              <CustomTable rows={rows} columns={columns} />
            </Box>
          </>
        )}
      </Box>
    </>
  );
};

export default AthleteDetailPage;
