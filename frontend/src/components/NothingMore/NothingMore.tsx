/** @format */

import { Alert, AlertTitle } from "@mui/material";
import React from "react";

const NothingMore: React.FC = () => {
  return (
    <Alert sx={{ m: 1 }} severity="success">
      <AlertTitle>That's the Final Attempt</AlertTitle>
      There are no more results to show.
    </Alert>
  );
};

export default NothingMore;
