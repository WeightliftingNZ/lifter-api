/** @format */

import React, { useState } from "react";
import { Tabs, Tab } from "@mui/material";
import Title from "../../components/Title";
import { Box } from "@mui/system";
import GeneralSearch from "./GeneralSearch";
import { useSearchParams } from "react-router-dom";

const SearchPage: React.FC = () => {
  const [tabValue, setTabValue] = useState<number>(0);
  const [searchParams] = useSearchParams();

  const handleOnTabChange = (event: React.SyntheticEvent, newValue: number) => {
    if (event) {
      setTabValue(newValue);
    }
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
      }}
    >
      <Title
        sx={{
          overflow: "hidden",
          maxWidth: "90vw",
          textOverflow: "ellipsis",
          whiteSpace: "nowrap",
        }}
      >
        Search: {searchParams.get("q")}
      </Title>
      <Tabs
        value={tabValue}
        onChange={handleOnTabChange}
        aria-label="athlete selection tabs"
      >
        <Tab label="General"></Tab>
        <Tab label="Athletes"></Tab>
        <Tab label="Competitions"></Tab>
      </Tabs>
      <Box>
        {tabValue === 0 && <GeneralSearch />}
        {tabValue === 1 && <Box>Athlete</Box>}
        {tabValue === 2 && <Box>Competition</Box>}
      </Box>
    </Box>
  );
};

export default SearchPage;
