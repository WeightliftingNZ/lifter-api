/** @format */

import { Link, TableCell } from "@mui/material";
import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { TableCellLinkProps } from "./interfaces";

const TableCellLink: React.FC<React.PropsWithChildren<TableCellLinkProps>> = (
  props
) => {
  return (
    <TableCell {...props.tableCellProps}>
      <Link
        sx={{
          display: "block",
          p: 1,
          textDecoration: "none",
          width: "100%",
          height: "100%",
          color: "inherit",
          overflow: "inherit",
          textOverflow: "inherit",
          maxWidth: "inherit",
        }}
        component={RouterLink}
        to={props.to || ""}
      >
        {props.children}
      </Link>
    </TableCell>
  );
};

export default TableCellLink;
