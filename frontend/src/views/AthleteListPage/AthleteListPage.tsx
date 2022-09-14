import React, { useState } from "react";
import { useQuery } from "react-query";
import { useDebounce } from "usehooks-ts";
import apiClient from "../../utils/http-common";
import Box from "@mui/material/Box";
import CustomError from "../../components/Error";
import CustomLoading from "../../components/Loading";
import {
  AthleteObjectProps,
  DRFPaginatedResponseProps,
} from "../../interfaces";
import CustomTable from "../../components/CustomTable";
import CustomSearchInput from "../../components/CustomSearchInput";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";

const COLUMNS_TO_SHOW: (keyof AthleteObjectProps)[] = [
  "first_name",
  "last_name",
  "yearborn",
];

interface DataLoaderProps {
  searchQuery?: string;
  page: number;
  handleChangePage: any; // TODO: Whatis this type?
  uriBase: "athletes" | "competitions";
}

const AthleteDataLoader: React.FC<DataLoaderProps> = ({
  searchQuery,
  page,
  handleChangePage,
  uriBase,
}) => {
  const debouncedSearchQuery = useDebounce(searchQuery, 500);

  const { data, isLoading, isError } = useQuery(
    [uriBase, debouncedSearchQuery + page.toString()],
    async () => {
      const res = await apiClient.get(
        `${uriBase}?page=${page + 1}&search=${searchQuery}`
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
  const rows: AthleteObjectProps[] = parsed_data.results;
  const nextPage = parsed_data.next;
  const previousPage = parsed_data.previous;
  const columns: (keyof AthleteObjectProps)[] = COLUMNS_TO_SHOW;
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
      uriBase={uriBase}
    />
  );
};

const AthleteListPage: React.FC = () => {
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
          Athlete
        </Typography>
        <Typography variant="subtitle2">Browse competition athletes</Typography>
      </Box>
      <Box sx={{ mt: 6 }}>
        <CustomSearchInput
          beingSearched="competitions"
          searchTerm={searchQuery}
          handleOnChange={handleOnChange}
        />
      </Box>
      <Box sx={{ mt: 6 }}>
        <AthleteDataLoader
          searchQuery={searchQuery}
          handleChangePage={handleChangePage}
          page={page}
          uriBase="athletes"
        />
      </Box>
    </>
  );
};

export default AthleteListPage;
