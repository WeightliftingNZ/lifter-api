import React from "react";
import { useDebounce } from "usehooks-ts";
import { useQuery } from "react-query";
import apiClient from "../../utils/http-common";
import CustomTable from "../CustomTable";
import CustomError from "../Error";
import CustomLoading from "../Loading";
import { DRFPaginatedResponseProps } from "../../interfaces";

interface DataLoaderProps {
  columnsToShow: any;
  setNoResults: React.Dispatch<React.SetStateAction<boolean | undefined>>;
  searchQuery?: string;
  page: number;
  handleChangePage: any; // TODO: type?
  dateAfter?: string;
  dateBefore?: string;
  uriBase: "athletes" | "competitions";
}

const DataLoader: React.FC<DataLoaderProps> = ({
  columnsToShow,
  searchQuery,
  page,
  handleChangePage,
  setNoResults,
  uriBase,
  dateAfter,
  dateBefore,
}) => {
  const debouncedSearchQuery = useDebounce(searchQuery, 500);

  const requestParams = [];

  const baseRequest = `${uriBase}?page=${page + 1}`;

  if (searchQuery) {
    requestParams.push(`&search=${searchQuery}`);
  }

  if (dateAfter || dateBefore) {
    requestParams.push(
      `&date_start_after=${dateAfter}&date_start_after=${dateBefore}`
    );
  }

  const request = baseRequest.concat(...requestParams);

  const { data, isLoading, isError } = useQuery(
    [uriBase, debouncedSearchQuery + page.toString()],
    async () => {
      const res = await apiClient.get(request);
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
    setNoResults(true);
    return <></>;
  }

  setNoResults(false);

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
