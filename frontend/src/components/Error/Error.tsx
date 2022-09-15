import React from "react";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";

const Error: React.FC = () => {
  return (
    <Box sx={{ width: "100%", height: "40%" }}>
      <Alert severity="error"> Error </Alert>
    </Box>
  );
};

export default Error;
