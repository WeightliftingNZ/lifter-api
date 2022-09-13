import React from "react";
import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import apiClient from "../../utils/http-common";
import CustomLoading from "../../components/Loading";
import CustomError from "../../components/Error";
import CustomTable from "./table";
import {
  CompetitionDetailObjectProps,
  LiftObjectProps,
} from "../../interfaces";
import Alert from "@mui/material/Alert";
import { dateTimeConverter } from "../../utils/customFunctions/customFunctions";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

const COLUMNS_TO_SHOW: (keyof LiftObjectProps)[] = [
  "lottery_number",
  "athlete_name",
  "total_lifted",
  "bodyweight",
  "weight_category",
  "team",
  "placing",
];

const CompetitionDetailPage: React.FC = () => {
  const params = useParams();
  const competitionId = params.competitionReferenceId;

  const { data, isLoading, isError } = useQuery(
    ["competitions", competitionId],
    async () => {
      const res = await apiClient.get(`/competitions/${competitionId}`);
      return res.data;
    }
  );
  if (isLoading) {
    return <CustomLoading />;
  }

  if (isError) {
    return <CustomError />;
  }

  const parsed_data: CompetitionDetailObjectProps = data;
  const rows: LiftObjectProps[] = parsed_data.lift_set;
  const columns: (keyof LiftObjectProps)[] = COLUMNS_TO_SHOW;
  const name: string = parsed_data.name;
  const date_start: string = parsed_data.date_start;
  const date_end: string = parsed_data.date_end;
  const lifts_count: number = parsed_data.lifts_count;

  if (rows.length === 0) {
    return <Alert severity="info">No Lifts Record for this Competition</Alert>;
  }

  return (
    <>
      <Box>
        <Typography variant="h4" gutterBottom>
          {name}
        </Typography>
        <Typography variant="subtitle2">
          {dateTimeConverter(date_start, false)}{" "}
          {dateTimeConverter(date_end, false)}
        </Typography>
        <Typography variant="subtitle2">
          Number of lifts: {lifts_count}
        </Typography>
      </Box>
      <Box sx={{ mt: 6 }}>
        <CustomTable rows={rows} columns={columns} />
      </Box>
    </>
  );
};

export default CompetitionDetailPage;
