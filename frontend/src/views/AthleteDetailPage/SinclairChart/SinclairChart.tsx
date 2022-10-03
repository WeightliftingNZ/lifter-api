/** @format */

import {
  Card,
  CardContent,
  CardHeader,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";
import { Box } from "@mui/system";
import moment from "moment";
import React from "react";
import {
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  XAxis,
  YAxis,
  Label,
} from "recharts";
import Heading from "../../../components/Heading";
import { LiftObjectProps } from "../../../interfaces";

/* TODO: types? */
const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload) return null;
  return (
    <Card>
      <CardHeader
        title={payload[0].payload.name}
        titleTypographyProps={{
          sx: {
            overflow: "hidden",
            maxWidth: "90%",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          },
        }}
        subheader={moment(payload[0].payload.date, "X").format("MMM Do, YYYY")}
      />
      <CardContent sx={{ display: "flex", justifyItems: "center" }}>
        <TableContainer>
          <Table padding="none" size="small">
            <TableHead></TableHead>
            <TableBody>
              <TableRow>
                <TableCell variant="head">Sinclair</TableCell>
                <TableCell>{payload[0].payload.sinclair}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell variant="head">S</TableCell>
                <TableCell>{payload[0].payload.snatch}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell variant="head">CJ</TableCell>
                <TableCell>{payload[0].payload.cnj}</TableCell>
              </TableRow>
              <TableRow>
                <TableCell variant="head">T</TableCell>
                <TableCell>{payload[0].payload.total}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
      </CardContent>
    </Card>
  );
};

interface SinclairChartProps {
  liftSet: LiftObjectProps[];
}

interface SinclairChartDataProps {
  name: string;
  snatch: number;
  cnj: number;
  total: number;
  sinclair: number;
  date: number | string;
}

const SinclairChart: React.FC<SinclairChartProps> = ({ liftSet }) => {
  const theme = useTheme();

  const chartData: SinclairChartDataProps[] = liftSet
    .filter((lift) => lift.total_lifted !== 0)
    .map((lift) => ({
      name: lift.competition_name,
      snatch: lift.best_snatch_weight[1],
      cnj: lift.best_cnj_weight[1],
      total: lift.total_lifted,
      sinclair: lift.sinclair,
      date: moment(lift.competition_date_start, "YYYY-MM-DD").format("X"),
    }));

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 1,
        overflowX: "scroll",
        whiteSpace: "nowrap",
        position: "relative",
        overflowY: "hidden",
      }}
    >
      <Heading>Sinclair</Heading>
      <ResponsiveContainer width="100%" height="100%" minHeight={400}>
        <ScatterChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="date"
            domain={["auto", "auto"]}
            name="Date"
            tickFormatter={(unixTime) =>
              moment(unixTime, "X").format("YYYY-MM-DD")
            }
            type="number"
          >
            <Label
              value="Competition Date"
              offset={-2}
              position="insideBottom"
            />
          </XAxis>
          <YAxis name="Sinclair" type="number"></YAxis>
          <Scatter
            dataKey="sinclair"
            line
            fill={theme.palette.primary.main}
            lineJointType="monotone"
            lineType="joint"
            name="Sinclair"
            type="number"
          />
          <Tooltip content={CustomTooltip} />
        </ScatterChart>
      </ResponsiveContainer>
    </Box>
  );
};
export default SinclairChart;
