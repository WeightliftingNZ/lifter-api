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
      variant="h6"
      gutterBottom
      sx={{ color: theme.palette.secondary.dark }}
      {...props}
    >
      {props.children}
    </Typography>
  );
};

export default Heading;
