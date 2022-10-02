/** @format */

import { Alert, AlertTitle } from "@mui/material";
import React from "react";

const NoResults: React.FC = () => {
  return (
    <Alert severity="info">
      <AlertTitle>Waiting for the down signal</AlertTitle>
      Pending results
    </Alert>
  );
};

export default NoResults;
