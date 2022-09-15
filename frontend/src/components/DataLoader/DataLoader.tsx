import React from "react";
import { useDebounce } from "usehooks-ts";
import { useQuery } from "react-query";
import apiClient from "../../utils/http-common";
import CustomTable from "../CustomTable";
import CustomError from "../Error";
import CustomLoading from "../Loading";
import { Alert } from "@mui/material";
import { DRFPaginatedResponseProps } from "../../interfaces";

interface DataLoaderProps {
  columnsToShow: any;
  searchQuery?: string;
  page: number;
  handleChangePage: any; // TODO: Whatis this type?
  uriBase: "athletes" | "competitions";
}

const DataLoader: React.FC<DataLoaderProps> = ({
  columnsToShow,
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
  const rows: any = parsed_data.results;
  const nextPage = parsed_data.next;
  const previousPage = parsed_data.previous;
  const columns: any = columnsToShow;
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

export default DataLoader;
