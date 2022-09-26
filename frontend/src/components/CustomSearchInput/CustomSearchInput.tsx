/** @format */

import React from "react";
import TextField from "@mui/material/TextField";
import SearchIcon from "@mui/icons-material/Search";
import IconButton from "@mui/material/IconButton";
import { InputAdornment } from "@mui/material";

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
    <TextField
      autoFocus
      id="search-box"
      label={label}
      error={error}
      color="secondary"
      placeholder={placeholder}
      helperText={helperText}
      onChange={handleOnChange}
      value={searchTerm}
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <IconButton color={error ? "error" : "default"}>
              <SearchIcon />
            </IconButton>
          </InputAdornment>
        ),
      }}
    />
  );
};

export default CustomSearchInput;
