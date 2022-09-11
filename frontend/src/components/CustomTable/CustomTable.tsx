import React, { useMemo, forwardRef } from "react";
import { styled, useTheme } from "@mui/material/styles";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableFooter from "@mui/material/TableFooter";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import TablePagination from "@mui/material/TablePagination";
import IconButton from "@mui/material/IconButton";
import FirstPageIcon from "@mui/icons-material/FirstPage";
import LastPageIcon from "@mui/icons-material/LastPage";
import KeyboardArrowLeft from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
}));

/* TODO: figure out how to make props into a list of predetermined strings
 * instead of using Record<string, any>  */
interface TableRowLinkProps extends Record<string, any> {}

const TableRowLink = (props: TableRowLinkProps) => {
  const theme = useTheme();
  const { columns, row } = props;
  const { reference_id } = row;

  const renderLink = useMemo(
    () =>
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(function Link(
        itemProps,
        ref
      ) {
        return (
          <RouterLink
            to={`/competitions/${reference_id}`}
            ref={ref}
            {...itemProps}
            role={undefined}
          />
        );
      }),
    [reference_id]
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

interface TablePaginationActionsProps {
  count: number;
  page: number;
  rowsPerPage: number;
  onPageChange: (
    event: React.MouseEvent<HTMLButtonElement>,
    newPage: number
  ) => void;
}

function titleMaker(title: string) {
  /* Turns titles into text (e.g. 'date_started' => 'Date Started')*/
  return title
    .replace("_", " ")
    .split(" ")
    .map((word) => {
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}

interface CustomTableProps {
  rows: any; // TODO: need to sort this type
  rowsPerPage: number;
  nextPage: string;
  previousPage: string;
  count: number;
  columns: any; // TODO: need to sort this type
  page: number;
  handleChangePage: any; // TODO: what type is this?
}

const CustomTable: React.FC<CustomTableProps> = (props: CustomTableProps) => {
  const {
    columns,
    rows,
    nextPage,
    previousPage,
    page,
    handleChangePage,
    count,
    rowsPerPage,
  } = props;

  /* TODO: only reason this compoenent is in here is because of nextPage and */
  /*     not being able to pass through */
  const TablePaginationActions = (props: TablePaginationActionsProps) => {
    const theme = useTheme();
    const { page, onPageChange, count, rowsPerPage } = props;

    const handleFirstPageButtonClick = (
      event: React.MouseEvent<HTMLButtonElement>
    ) => {
      onPageChange(event, 0);
    };
    const handleBackButtonClick = (
      event: React.MouseEvent<HTMLButtonElement>
    ) => {
      onPageChange(event, page - 1);
    };
    const handleNextButtonClick = (
      event: React.MouseEvent<HTMLButtonElement>
    ) => {
      onPageChange(event, page + 1);
    };
    const handleLastPageButtonClick = (
      event: React.MouseEvent<HTMLButtonElement>
    ) => {
      onPageChange(event, Math.max(0, Math.floor(count / rowsPerPage)));
    };

    return (
      <Box sx={{ flexShrink: 0, ml: 2.5 }}>
        <IconButton
          onClick={handleFirstPageButtonClick}
          disabled={previousPage == null}
          aria-label="first page"
        >
          {theme.direction === "rtl" ? <LastPageIcon /> : <FirstPageIcon />}
        </IconButton>
        <IconButton
          onClick={handleBackButtonClick}
          disabled={previousPage == null}
          aria-label="back page"
        >
          {theme.direction === "rtl" ? (
            <KeyboardArrowRight />
          ) : (
            <KeyboardArrowLeft />
          )}
        </IconButton>
        <IconButton
          onClick={handleNextButtonClick}
          disabled={nextPage == null}
          aria-label="next page"
        >
          {theme.direction === "rtl" ? (
            <KeyboardArrowLeft />
          ) : (
            <KeyboardArrowRight />
          )}
        </IconButton>
        <IconButton
          onClick={handleLastPageButtonClick}
          disabled={nextPage == null}
          aria-label="last page"
        >
          {theme.direction === "rtl" ? <FirstPageIcon /> : <LastPageIcon />}
        </IconButton>
      </Box>
    );
  };
  return (
    <TableContainer component={Paper}>
      <Table stickyHeader sx={{ minWidth: 650 }} aria-label="Competition Table">
        <TableHead>
          <TableRow>
            {columns.map((column: string, idx: number) => (
              <StyledTableCell key={idx}>{titleMaker(column)}</StyledTableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {/* TODO: fix row type */}
          {rows.map((row: any, idx: number) => (
            <TableRowLink
              key={idx}
              /* TODO: find out a way to now have to declare each prop */
              row={row}
              columns={columns}
            />
          ))}
        </TableBody>
      </Table>
      <TableFooter>
        <TableRow>
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
        </TableRow>
      </TableFooter>
    </TableContainer>
  );
};

export default CustomTable;
