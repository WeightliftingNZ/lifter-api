/** @format */

import React from "react";
import { Typography } from "@mui/material";

interface BodyProps {
  children?: React.ReactNode;
}

const Body: React.FC<React.PropsWithChildren<BodyProps>> = (
  props: BodyProps
) => {
  return (
    <Typography variant="body1" gutterBottom noWrap {...props}>
      {props.children}
    </Typography>
  );
};

export default Body;
