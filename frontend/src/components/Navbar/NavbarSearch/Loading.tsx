/** @format */

import { LinearProgress, Skeleton } from "@mui/material";
import { Box } from "@mui/system";
import React from "react";

const Loading: React.FC = () => {
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 4,
        justifySelf: "auto",
      }}
    >
      <>
        <LinearProgress color="secondary" />
        {Array.from(Array(4).keys()).map((idx: number) => {
          return (
            <Box
              key={idx}
              sx={{ display: "flex", justifyContent: "space-between" }}
            >
              <Skeleton sx={{ flexGrow: 4 }} animation="wave" />
              <Box sx={{ flexGrow: 1 }} />
              <Skeleton sx={{ flexGrow: 4 }} animation="wave" />
              <Box sx={{ flexGrow: 3 }} />
              <Skeleton sx={{ flexGrow: 2 }} animation="wave" />
            </Box>
          );
        })}
      </>
    </Box>
  );
};

export default Loading;
