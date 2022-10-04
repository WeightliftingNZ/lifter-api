/** @format */

import { LinkProps } from "@mui/material";

interface TableCellLinkProps extends LinkProps {
  to?: string | { pathname: string; hash: string };
  tableCellProps?: TableCellProps;
  children?: React.ReactNode;
}
