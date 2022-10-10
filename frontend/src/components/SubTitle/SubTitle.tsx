/** @format */

import React from "react";
import { Typography, TypographyProps } from "@mui/material";

interface SubTitleProps extends TypographyProps {
  children?: React.ReactNode;
}

const SubTitle: React.FC<React.PropsWithChildren<SubTitleProps>> = (
  props: SubTitleProps
) => {
  return (
    <Typography color="primary" variant="subtitle2" {...props}>
      {props.children}
    </Typography>
  );
};

export default SubTitle;
