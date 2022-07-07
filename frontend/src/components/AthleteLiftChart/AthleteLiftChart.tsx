import React from "react";
import { AxisOptions, Chart } from "react-charts";

type ChartDatum = {
    date: Date,
    stars: number
}

const AthletePreviousLifts = () => {
  const data = [
    {
      label: "Test",
      data: [
        {
          date: new Date(),
          starts: 101212,
        },
      ],
    },
  ];

  const primaryAxis = React.useMemo(
    (): AxisOptions<ChartDatum> => ({
      getValue: (datum) => datum.date,
    }),
    []
  );
  const secondaryAxis = React.useMemo(
    (): AxisOptions<ChartDatum> => ({
      getValue: (datum) => datum.stars,
    }),
    []
  );
  return (
      <Chart options={{
          data,
          primaryAxis,
          secondaryAxis
      }}
};

export default AthletePreviousLifts;
