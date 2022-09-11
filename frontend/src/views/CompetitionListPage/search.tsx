import React from "react";
import TextField from "@mui/material/TextField";
import SearchIcon from "@mui/icons-material/Search";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";

interface SearchBoxProps {
  beingSearched: "competitions" | "athletes";
  searchTerm?: string;
  handleOnChange: any; // TODO: what type is this?
}

const SearchInput: React.FC<SearchBoxProps> = (props: SearchBoxProps) => {
  const { searchTerm, handleOnChange, beingSearched } = props;
  return (
    <Stack direction="row" alignItems="center" spacing={2}>
      <TextField
        autoFocus
        sx={{ minWidth: 450, maxWidth: 750 }}
        id="search-box"
        label={`Search ${beingSearched}`}
        onChange={handleOnChange}
        value={searchTerm}
      />
      <IconButton>
        <SearchIcon />
      </IconButton>
    </Stack>
  );
};

export default SearchInput;
