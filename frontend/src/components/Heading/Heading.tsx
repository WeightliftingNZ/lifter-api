/** @format */

import React from "react";
import { Typography } from "@mui/material";
import { useTheme } from "@mui/material/styles";

interface HeadingProps {
  children?: React.ReactNode;
}

const Heading: React.FC<React.PropsWithChildren<HeadingProps>> = (
  props: HeadingProps
) => {
  const theme = useTheme();
  return (
    <Typography
      variant="h4"
      gutterBottom
      sx={{ p: 1, color: theme.palette.secondary.dark }}
      {...props}
    >
      {props.children}
    </Typography>
  );
};

export default Heading;
