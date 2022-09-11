import React, { useState } from "react";
import { useQuery } from "react-query";
import { useDebounce } from "usehooks-ts";
import apiClient from "../../utils/http-common";
import Box from "@mui/material/Box";
import CustomError from "../../components/Error";
import CustomLoading from "../../components/Loading";
import { DRFPaginatedResponseProps } from "../../interfaces";
import { CompetitionObjectPropsKeys } from "./interfaces";
import CompetitionListTable from "./table";
import SearchInput from "./search";

const COLUMNS_TO_SHOW: CompetitionObjectPropsKeys[] = [
  "name",
  "date_start",
  "lifts_count",
  "location",
];

interface FooProps {
  searchQuery?: string;
  page: number;
  handleChangePage: any; // TODO: Whatis this type?
}
const Foo: React.FC<FooProps> = ({ searchQuery, page, handleChangePage }) => {
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
  const rows = parsed_data.results;
  const nextPage = parsed_data.next;
  const previousPage = parsed_data.previous;
  const columns: CompetitionObjectPropsKeys[] = COLUMNS_TO_SHOW;
  const rowsPerPage = parsed_data.per_page;
  const count = parsed_data.count;

  console.log("page", page);

  return (
    <Box sx={{ mt: 6 }}>
      <CompetitionListTable
        page={page}
        count={count}
        nextPage={nextPage}
        previousPage={previousPage}
        rowsPerPage={rowsPerPage}
        handleChangePage={handleChangePage}
        rows={rows}
        columns={columns}
      />
    </Box>
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
        <h2>Competition</h2>
        <h4>Browse competition results</h4>
      </Box>
      <Box sx={{ mt: 6 }}>
        <SearchInput
          beingSearched="competitions"
          searchTerm={searchQuery}
          handleOnChange={handleOnChange}
        />
      </Box>
      <Foo
        searchQuery={searchQuery}
        handleChangePage={handleChangePage}
        page={page}
      />
    </>
  );
};

export default CompetitionListPage;
