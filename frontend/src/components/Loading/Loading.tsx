import React, { useEffect } from "react";
import LinearProgress from "@mui/material/LinearProgress";
import Box from "@mui/material/Box";

const Loading = () => {
  return (
    <Box sx={{ width: "100%", height: "20%" }}>
      <LinearProgress />
    </Box>
  );
};

export default Loading;
