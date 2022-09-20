import React from "react";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableFooter from "@mui/material/TableFooter";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TablePagination from "@mui/material/TablePagination";
import TableRowLink from "./tableRowLink";
import { StyledTableCell } from "./customStyles";
import TablePaginationActions from "./tablePaginationActions";

interface RowProps extends Record<string, any> {}

interface CustomTableProps {
  rows: RowProps[]; // TODO: need to sort this type
  rowsPerPage: number;
  nextPage: string;
  previousPage: string;
  count: number;
  columns: any; // TODO: need to sort this type
  page: number;
  handleChangePage: any; // TODO: what type is this?
  uriBase: "competitions" | "athletes";
}

const CustomTable: React.FC<CustomTableProps> = (props: CustomTableProps) => {
  const { columns, rows, page, handleChangePage, count, rowsPerPage, uriBase } =
    props;

  return (
    <>
      <TableContainer
        component={Paper}
        sx={{
          marginLeft: "auto",
          marginRight: "auto",
        }}
      >
        <Table stickyHeader aria-label="Custom Table">
          <TableHead>
            <TableRow>
              {columns.map((column: any) => (
                <StyledTableCell key={column.id}>
                  {column.label}
                </StyledTableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {/* TODO: fix row type */}
            {rows.map((row: RowProps, idx: number) => (
              <TableRowLink
                key={idx}
                row={row}
                columns={columns}
                uriBase={uriBase}
              />
            ))}
          </TableBody>
          <TableFooter>
            <TablePagination
              rowsPerPageOptions={[]}
              count={count}
              rowsPerPage={rowsPerPage}
              page={page}
              SelectProps={{
                inputProps: {
                  "aria-label": "rows per page",
                },
                native: true,
              }}
              onPageChange={handleChangePage}
              ActionsComponent={TablePaginationActions}
            />
          </TableFooter>
        </Table>
      </TableContainer>
    </>
  );
};

export default CustomTable;
