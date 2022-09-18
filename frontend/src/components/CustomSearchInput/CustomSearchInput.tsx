import React from "react";
import TextField from "@mui/material/TextField";
import SearchIcon from "@mui/icons-material/Search";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";

interface CustomSearchInputProps {
  error?: boolean;
  label?: string;
  placeholder?: string;
  helperText?: string;
  searchTerm?: string;
  handleOnChange: React.ChangeEventHandler<HTMLInputElement>;
}

const CustomSearchInput: React.FC<CustomSearchInputProps> = (
  props: CustomSearchInputProps
) => {
  const { searchTerm, handleOnChange, label, placeholder, helperText, error } =
    props;
  return (
    <Stack direction="row" alignItems="center" spacing={2}>
      <TextField
        autoFocus
        sx={{ minWidth: 450, maxWidth: 750 }}
        id="search-box"
        label={label}
        error={error}
        color="secondary"
        placeholder={placeholder}
        helperText={helperText}
        onChange={handleOnChange}
        value={searchTerm}
      />
      <IconButton color={error ? "error" : "default"}>
        <SearchIcon />
      </IconButton>
    </Stack>
  );
};

export default CustomSearchInput;
