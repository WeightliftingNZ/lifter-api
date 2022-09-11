import React from "react";
import LinearProgress from "@mui/material/LinearProgress";
import Box from "@mui/material/Box";
import Skeleton from "@mui/material/Skeleton";

const Loading: React.FC = () => {
  return (
    <Box sx={{ width: "100%", height: "20%" }}>
      <Skeleton />
      <LinearProgress />
    </Box>
  );
};

export default Loading;
