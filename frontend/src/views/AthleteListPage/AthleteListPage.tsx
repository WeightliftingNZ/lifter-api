import React, { useState } from "react";
import Box from "@mui/material/Box";
import { AthleteListObjectProps } from "../../interfaces";
import CustomSearchInput from "../../components/CustomSearchInput";
import DataLoader from "../../components/DataLoader";
import Title from "../../components/Title";
import SubTitle from "../../components/SubTitle";

const COLUMNS_TO_SHOW: (keyof AthleteListObjectProps)[] = [
  "first_name",
  "last_name",
  "yearborn",
];

/* TODO: refactor list tables */
/* export interface Column { */
/*   id: keyof AthleteListObjectProps; */
/*   label: string; */
/*   minWidth?: number; */
/*   maxWidth?: number; */
/*   align?: "right" | "left" | "center"; */
/*   format?: (value: number) => string; */
/*   extra?: { [key: string]: string }; */
/* } */
/**/
/* const columns: Column[] = [ */
/*   { id: "first_name", label: "First Name", maxWidth: 100 }, */
/*   { id: "last_name", label: "Last Name" }, */
/* ]; */

const AthleteListPage: React.FC = () => {
  const [page, setPage] = useState<number>(0);
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [noResults, setNoResults] = useState<boolean | undefined>();

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
        <Title>Athlete</Title>
        <SubTitle>Browse athletes</SubTitle>
      </Box>
      <Box sx={{ mt: 6 }}>
        <CustomSearchInput
          error={noResults}
          label="Search athletes"
          placeholder="By first or last name"
          helperText={noResults ? "No results found" : ""}
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
          uriBase="athletes"
        />
      </Box>
    </>
  );
};

export default AthleteListPage;
