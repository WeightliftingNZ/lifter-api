import React, { useState } from "react";
import { useQuery } from "react-query";
import { useDebounce } from "usehooks-ts";
import apiClient from "../../utils/http-common";
import Box from "@mui/material/Box";
import CustomError from "../../components/Error";
import CustomLoading from "../../components/Loading";
import {
  CompetitionObjectProps,
  DRFPaginatedResponseProps,
} from "../../interfaces";
import CustomTable from "../../components/CustomTable";
import CustomSearchInput from "../../components/CustomSearchInput";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";

const COLUMNS_TO_SHOW: (keyof CompetitionObjectProps)[] = [
  "name",
  "date_start",
  "lifts_count",
  "location",
];

interface CompetitionDataLoaderProps {
  searchQuery?: string;
  page: number;
  handleChangePage: any; // TODO: Whatis this type?
}

const CompetitionDataLoader: React.FC<CompetitionDataLoaderProps> = ({
  searchQuery,
  page,
  handleChangePage,
}) => {
  const debouncedSearchQuery = useDebounce(searchQuery, 500);

  const { data, isLoading, isError } = useQuery(
    ["competitions", debouncedSearchQuery + page.toString()],
    async () => {
      const res = await apiClient.get(
        `/competitions?page=${page + 1}&search=${searchQuery}`
      );
      return res.data;
    }
  );
  if (isLoading) {
    return <CustomLoading />;
  }

  if (isError) {
    return <CustomError />;
  }
  const parsed_data: DRFPaginatedResponseProps = data;
  const rows: CompetitionObjectProps[] = parsed_data.results;
  const nextPage = parsed_data.next;
  const previousPage = parsed_data.previous;
  const columns: (keyof CompetitionObjectProps)[] = COLUMNS_TO_SHOW;
  const rowsPerPage = parsed_data.per_page;
  const count = parsed_data.count;

  if (rows.length === 0) {
    return <Alert severity="info">No Results for "{searchQuery}"</Alert>;
  }

  return (
    <CustomTable
      page={page}
      count={count}
      nextPage={nextPage}
      previousPage={previousPage}
      rowsPerPage={rowsPerPage}
      handleChangePage={handleChangePage}
      rows={rows}
      columns={columns}
    />
  );
};

const CompetitionListPage: React.FC = () => {
  const [page, setPage] = useState(0);
  const [searchQuery, setSearchQuery] = useState("");

  /* TODO: event type? */
  const handleOnChange = (event: any) => {
    setSearchQuery(event.target.value);
    setPage(0);
  };

  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number
  ) => {
    setPage(newPage);
  };

  return (
    <>
      <Box>
        <Typography variant="h4" gutterBottom>
          Competition
        </Typography>
        <Typography variant="subtitle2">Browse competition results</Typography>
      </Box>
      <Box sx={{ mt: 6 }}>
        <CustomSearchInput
          beingSearched="competitions"
          searchTerm={searchQuery}
          handleOnChange={handleOnChange}
        />
      </Box>
      <Box sx={{ mt: 6 }}>
        <CompetitionDataLoader
          searchQuery={searchQuery}
          handleChangePage={handleChangePage}
          page={page}
        />
      </Box>
    </>
  );
};

export default CompetitionListPage;
