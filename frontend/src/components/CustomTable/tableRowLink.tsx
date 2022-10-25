/** @format */

import React, { forwardRef, useMemo } from "react";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";
import { useTheme } from "@mui/material/styles";
import TableRow from "@mui/material/TableRow";
import { StyledTableCell } from "./customStyles";
import { grey } from "@mui/material/colors";
import { Typography } from "@mui/material";

/* TODO: figure out how to make props into a list of predetermined strings
 * instead of using Record<string, any>  */
interface TableRowLinkProps extends Record<string, any> {}

const TableRowLink: React.FC<TableRowLinkProps> = (
  props: TableRowLinkProps
) => {
  const theme = useTheme();
  const { columns, row, uriBase } = props;
  const { reference_id } = row;

  const renderLink = useMemo(
    () =>
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(
        function Link(itemProps, ref) {
          return (
            <RouterLink
              to={`/${uriBase}/${reference_id}`}
              ref={ref}
              {...itemProps}
              role={undefined}
              style={{ textDecoration: "none" }}
            />
          );
        }
      ),
    [uriBase, reference_id]
  );

  return (
    <TableRow
      sx={{
        "&:nth-of-type(odd)": {
          backgroundColor: grey[200],
        },
        "&:last-child td, &:last-child th": {
          border: 0,
        },
        "&:hover td": {
          backgroundColor: theme.palette.secondary.light,
        },
      }}
      component={renderLink}
    >
      {columns.map((column: any) => {
        return (
          <StyledTableCell key={column.id}>
            <Typography variant="h6">{row[column.id]}</Typography>
          </StyledTableCell>
        );
      })}
    </TableRow>
  );
};

export default TableRowLink;
