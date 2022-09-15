import React, { forwardRef, useMemo } from "react";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";
import { useTheme } from "@mui/material/styles";
import TableRow from "@mui/material/TableRow";
import { StyledTableCell } from "./customStyles";

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
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(function Link(
        itemProps,
        ref
      ) {
        return (
          /* TODO: URL is competitions but does not respect athlete etc */
          <RouterLink
            to={`/${uriBase}/${reference_id}`}
            ref={ref}
            {...itemProps}
            role={undefined}
            style={{ textDecoration: "none" }}
          />
        );
      }),
    [uriBase, reference_id]
  );

  return (
    <TableRow
      sx={{
        "&:nth-of-type(odd)": {
          backgroundColor: theme.palette.action.hover,
        },
        "&:last-child td, &:last-child th": {
          border: 0,
        },
      }}
      component={renderLink}
    >
      {columns.map((column: string, idx: number) => (
        <StyledTableCell key={idx}>{row[column]}</StyledTableCell>
      ))}
    </TableRow>
  );
};

export default TableRowLink;
