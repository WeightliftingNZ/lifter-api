/** @format */

import { ButtonProps } from "@mui/material";

export interface ButtonLinkProps extends ButtonProps {
  to: string;
  children?: React.ReactNode;
}
