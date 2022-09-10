import React, { forwardRef, useMemo, useState } from "react";
import { useQuery } from "react-query";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";
import apiClient from "../../utils/http-common";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableFooter from "@mui/material/TableFooter";
import TableCell, { tableCellClasses } from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Alert from "@mui/material/Alert";
import { useTheme, styled } from "@mui/material/styles";
import TablePagination from "@mui/material/TablePagination";
import IconButton from "@mui/material/IconButton";
import FirstPageIcon from "@mui/icons-material/FirstPage";
import LastPageIcon from "@mui/icons-material/LastPage";
import KeyboardArrowLeft from "@mui/icons-material/KeyboardArrowLeft";
import KeyboardArrowRight from "@mui/icons-material/KeyboardArrowRight";
import Loading from "../../components/Loading";
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import { CompetitionObjectProps } from "../../interfaces";

const COMPETITION_PAGINATION = 20;

const StyledTableCell = styled(TableCell)(({ theme }) => ({
  [`&.${tableCellClasses.head}`]: {
    backgroundColor: theme.palette.common.black,
    color: theme.palette.common.white,
  },
}));

interface CompetitionListTableProps
  extends Omit<CompetitionObjectProps, "date_end" | "url"> {}

interface TableRowLinkProps extends CompetitionListTableProps {
  [key: string]: any;
  columns: string[];
}

type CompetitionObjectPropsKeys = keyof CompetitionListTableProps;

const TableRowLink = (props: TableRowLinkProps) => {
  const theme = useTheme();
  const { reference_id, columns } = props;

  console.log(props);
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
      {/* Map this props */}
      {columns.map((column: any) => (
        <StyledTableCell>{props[column]}</StyledTableCell>
      ))}
    </TableRow>
  );
};

interface TablePaginationActionsProps {
  count: number;
  page: number;
  onPageChange: (
    event: React.MouseEvent<HTMLButtonElement>,
    newPage: number
  ) => void;
}

const titlizeKeys = (title: string) => {
  /* Turns titles into text (e.g. 'date_started' => 'Date Started')*/
  return title
    .replace("_", " ")
    .split(" ")
    .map((word) => {
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
};

const CompetitionListPage: React.FC = () => {
  const theme = useTheme();
  const [page, setPage] = useState(0);
  const [searchTerm, setSearchTerm] = useState(null);

  const handleSearchTermOnChange = (event: any) => {
    setSearchTerm(event.target.value);
  };

  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number
  ) => {
    setPage(newPage);
  };
  const { data, isLoading, isError } = useQuery(
    ["competitions", page],
    async () => {
      const res = await apiClient.get(
        `/competitions?page=${page + 1}&search=${searchTerm}`
      );
      return res.data;
    },
    { keepPreviousData: true }
  );

  if (isLoading) {
    return <Loading />;
  }

  if (isError) {
    return (
      <>
        <Box sx={{ width: "100%", height: "40%" }}>
          <Alert severity="error"> Error </Alert>
        </Box>
      </>
    );
  }
  const rows = data?.results;
  const columns: CompetitionObjectPropsKeys[] = [
    "name",
    "date_start",
    "lifts_count",
    "location",
  ];

  const nextPage = data?.next;
  const prevPage = data?.previous;

  const TablePaginationActions = (props: TablePaginationActionsProps) => {
    const theme = useTheme();
    const { page, onPageChange } = props;

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
      onPageChange(
        event,
        Math.max(0, Math.floor(data?.count / COMPETITION_PAGINATION))
      );
    };

    return (
      <Box sx={{ flexShrink: 0, ml: 2.5 }}>
        <IconButton
          onClick={handleFirstPageButtonClick}
          disabled={prevPage == null}
          aria-label="first page"
        >
          {theme.direction === "rtl" ? <LastPageIcon /> : <FirstPageIcon />}
        </IconButton>
        <IconButton
          onClick={handleBackButtonClick}
          disabled={prevPage == null}
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
    <>
      <Box sx={{ mt: 6 }}>
        <Box sx={{ mt: 12 }}>
          <h2>Competition</h2>
          <h4>Browse competition results</h4>
          <Autocomplete
            freeSolo
            id="search"
            sx={{ maxWidth: 500 }}
            value={searchTerm}
            onChange={handleSearchTermOnChange}
            options={rows.map((item: any) => item.name)}
            renderInput={(params) => <TextField {...params} label="Filter" />}
          />
        </Box>
        <Box sx={{ mt: 6 }}>
          <TableContainer component={Paper}>
            <Table
              stickyHeader
              sx={{ minWidth: 650 }}
              aria-label="Competition Table"
            >
              <TableHead>
                <TableRow>
                  {columns.map((column: string, idx: number) => (
                    <StyledTableCell key={idx}>
                      {titlizeKeys(column)}
                    </StyledTableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {rows.map((row: CompetitionObjectProps, idx: number) => (
                  <TableRowLink
                    lifts_count={row.lifts_count}
                    reference_id={row.reference_id}
                    date_start={row.date_start}
                    location={row.location}
                    name={row.name}
                    columns={columns}
                  />
                ))}
              </TableBody>
            </Table>
            <TableFooter>
              <TableRow>
                <TablePagination
                  rowsPerPageOptions={[]}
                  count={data?.count}
                  rowsPerPage={COMPETITION_PAGINATION}
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
        </Box>
      </Box>
    </>
  );
};

export default CompetitionListPage;
