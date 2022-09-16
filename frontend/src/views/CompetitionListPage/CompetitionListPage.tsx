import React, { useState } from "react";
import Box from "@mui/material/Box";
import CustomSearchInput from "../../components/CustomSearchInput";
import DataLoader from "../../components/DataLoader";
import { CompetitionListObjectProps } from "../../interfaces";
import Title from "../../components/Title";
import SubTitle from "../../components/SubTitle";

const COLUMNS_TO_SHOW: (keyof CompetitionListObjectProps)[] = [
  "name",
  "date_start",
  "lifts_count",
  "location",
];

const CompetitionListPage: React.FC = () => {
  const [page, setPage] = useState<number>(0);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [noResults, setNoResults] = useState<boolean | undefined>();

  /* TODO: event type? */
  const handleOnChange = (event: any) => {
    setSearchQuery(event.target.value);
    setPage(0);
  };

  /* TODO: event type? */
  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number
  ) => {
    setPage(newPage);
  };

  return (
    <>
      <Box>
        <Title>Competition</Title>
        <SubTitle>Browse competition results</SubTitle>
      </Box>
      <Box sx={{ mt: 6 }}>
        <CustomSearchInput
          error={noResults}
          label="Search competitions"
          helperText={noResults ? "No results found" : ""}
          placeholder="By name and/or location"
          searchTerm={searchQuery}
          handleOnChange={handleOnChange}
        />
      </Box>
      <Box sx={{ mt: 6 }}>
        <DataLoader
          setNoResults={setNoResults}
          columnsToShow={COLUMNS_TO_SHOW}
          searchQuery={searchQuery}
          handleChangePage={handleChangePage}
          page={page}
          uriBase="competitions"
        />
      </Box>
    </>
  );
};

export default CompetitionListPage;
