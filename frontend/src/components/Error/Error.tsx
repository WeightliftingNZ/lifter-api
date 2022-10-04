/** @format */

import React from "react";
import { Alert, Box, AlertTitle } from "@mui/material";
import FluorescentIcon from "@mui/icons-material/Fluorescent";

const Error: React.FC = () => {
  return (
    <Box sx={{ maxWidth: "fit-content" }}>
      <Alert
        icon={
          <Box sx={{ display: "flex", flexDirection: "column" }}>
            <FluorescentIcon fontSize="inherit" />
            <FluorescentIcon fontSize="inherit" />
            <FluorescentIcon
              sx={{
                animation: "blink-animation",
              }}
              fontSize="inherit"
            />
          </Box>
        }
        severity="error"
      >
        <AlertTitle> Three Red Lights </AlertTitle>
        Something went wrong. Please try again later.
      </Alert>
    </Box>
  );
};

export default Error;
