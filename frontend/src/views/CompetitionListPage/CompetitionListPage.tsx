import React, { useState } from "react";
import Box from "@mui/material/Box";
import CustomSearchInput from "../../components/CustomSearchInput";
import Typography from "@mui/material/Typography";
import DataLoader from "../../components/DataLoader";
import { CompetitionListObjectProps } from "../../interfaces";

const COLUMNS_TO_SHOW: (keyof CompetitionListObjectProps)[] = [
  "name",
  "date_start",
  "lifts_count",
  "location",
];

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
        <DataLoader
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
