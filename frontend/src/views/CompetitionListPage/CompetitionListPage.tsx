import React, { useState } from "react";
import Box from "@mui/material/Box";
import CustomSearchInput from "../../components/CustomSearchInput";
import DataLoader from "../../components/DataLoader";
import { CompetitionListObjectProps } from "../../interfaces";
import Title from "../../components/Title";
import SubTitle from "../../components/SubTitle";

export interface Column {
  id: keyof CompetitionListObjectProps;
  label: string;
  minWidth?: number;
  maxWidth?: number;
  align?: "right" | "left" | "center";
  format?: (value: number) => string;
  extra?: { [key: string]: string };
}

const columns: Column[] = [
  { id: "name", label: "Name" },
  { id: "location", label: "Location" },
  { id: "date_start", label: "Date" },
  { id: "lifts_count", label: "Athletes" },
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
          columns={columns}
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
