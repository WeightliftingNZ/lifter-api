/** @format */

import { Card, CardContent, Paper, Typography, useTheme } from "@mui/material";
import { Box, Stack } from "@mui/system";
import moment from "moment";
import React from "react";
import {
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  XAxis,
  YAxis,
} from "recharts";
import Title from "../../../components/Title";
import { LiftChartProps } from "./interfaces";

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

const SinclairChart: React.FC<LiftChartProps> = ({ data }) => {
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
export default SinclairChart;
