import React from "react";
import { useQuery } from "react-query";
import { useDebounce } from "usehooks-ts";
import apiClient from "../../utils/http-common";
import CustomError from "../../components/Error";
import CustomLoading from "../../components/Loading";
import {
  CompetitionListObjectProps,
  DRFPaginatedResponseProps,
} from "../../interfaces";
import CustomTable from "../../components/CustomTable";
import Alert from "@mui/material/Alert";
import { COLUMNS_TO_SHOW } from "./constants";

interface CompetitionDataLoaderProps {
  searchQuery?: string;
  page: number;
  handleChangePage: any; // TODO: Whatis this type?
  uriBase: "athletes" | "competitions";
}

const CompetitionDataLoader: React.FC<CompetitionDataLoaderProps> = ({
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
        `/${uriBase}?page=${page + 1}&search=${searchQuery}`
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
  const rows: CompetitionListObjectProps[] = parsed_data.results;
  const nextPage = parsed_data.next;
  const previousPage = parsed_data.previous;
  const columns: (keyof CompetitionListObjectProps)[] = COLUMNS_TO_SHOW;
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

export default CompetitionDataLoader;
