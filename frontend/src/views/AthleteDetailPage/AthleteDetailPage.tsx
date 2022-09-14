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

const columns: Column[] = [
  { id: "placing", label: "Lott." },
  { id: "competition_name", label: "Competition" },
  { id: "competition_date_start", label: "Date" },
  { id: "team", label: "Team" },
  { id: "bodyweight", label: "Weight" },
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
          <CustomTable rows={rows} columns={columns} />
        )}
      </Box>
    </>
  );
};

export default AthleteDetailPage;
