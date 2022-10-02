/** @format */

import React from "react";
import { Typography, TypographyProps } from "@mui/material";

interface TitleProps extends TypographyProps {
  children?: React.ReactNode;
}

const Title: React.FC<React.PropsWithChildren<TitleProps>> = (
  props: TitleProps
) => {
  return (
    <Typography color="primary" variant="h2" gutterBottom {...props}>
      {props.children}
    </Typography>
  );
};

export default Title;
