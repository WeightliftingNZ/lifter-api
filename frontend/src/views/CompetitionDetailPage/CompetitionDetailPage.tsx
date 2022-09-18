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
  "sinclair",
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

  const parsedData: CompetitionDetailObjectProps = data;
  const rows: LiftObjectProps[] = parsedData.lift_set;
  const columns: (keyof LiftObjectProps)[] = COLUMNS_TO_SHOW;
  const name: string = parsedData.name;
  const dateStart: string = parsedData.date_start;
  const dateEnd: string = parsedData.date_end;
  const liftCounts: number = parsedData.lifts_count;

  return (
    <>
      <Box>
        <Typography variant="h4" gutterBottom>
          {name}
        </Typography>
        <Typography variant="subtitle2">
          {dateTimeConverter(dateStart, false)}
          {dateStart !== dateEnd
            ? ` - ${dateTimeConverter(dateEnd, false)}`
            : ""}
        </Typography>
        <Typography variant="subtitle2">
          Number of lifts: {liftCounts}
        </Typography>
      </Box>
      <Box sx={{ mt: 6 }}>
        {rows.length === 0 ? (
          <Alert severity="info">
            No lifts recorded for "{name}" competition
          </Alert>
        ) : (
          <CustomTable rows={rows} columns={columns} />
        )}
      </Box>
    </>
  );
};

export default CompetitionDetailPage;
