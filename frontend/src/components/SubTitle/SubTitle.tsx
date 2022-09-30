/** @format */

import React from "react";
import { Typography } from "@mui/material";

interface SubTitleProps {
  children?: React.ReactNode;
}

const SubTitle: React.FC<React.PropsWithChildren<SubTitleProps>> = (
  props: SubTitleProps
) => {
  return (
    <Typography component="h6" color="primary" variant="subtitle2">
      {props.children}
    </Typography>
  );
};

export default SubTitle;
