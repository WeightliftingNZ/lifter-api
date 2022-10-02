/** @format */

import React, { useState } from "react";
import { useDebounce } from "usehooks-ts";
import {
  Autocomplete,
  InputAdornment,
  ListItem,
  ListItemButton,
  TextField,
} from "@mui/material";
import { useQuery } from "react-query";
import { useNavigate } from "react-router-dom";
import apiClient from "../../../utils/http-common/http-common";
import { useTheme } from "@mui/material/styles";
import SearchIcon from "@mui/icons-material/Search";
import Loading from "./Loading";
import { SearchResultProps } from "../../../interfaces";
import IconButtonLink from "../../IconButtonLink";
import { NavbarSearchProps } from "./interfaces";

const NavbarSearch: React.FC<NavbarSearchProps> = ({ handleSearchOnBlur }) => {
  const [value, setValue] = useState<string | null>("");
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [open, setOpen] = useState<boolean>(false);
  const navigate = useNavigate();
  const debouncedSearchQuery = useDebounce(searchQuery, 500);
  const theme = useTheme();

  const fetchSearchResults = async () => {
    const PAGE_LIMIT = 10;
    const res = await apiClient.get(
      `/search?q=${debouncedSearchQuery}&page_limit=${PAGE_LIMIT}`
    );
    return res.data;
  };

  const { data, error, isLoading, isError } = useQuery(
    ["navbarSearch", debouncedSearchQuery],
    () => fetchSearchResults(),
    { enabled: debouncedSearchQuery ? true : false }
  );

  if (isError) {
    console.log(error);
  }

  // Open popper
  const handleOnOpen = () => setOpen(true);

  const handleOnClose = () => setOpen(false);

  const handleOnInputChange = (
    event: React.SyntheticEvent,
    newInputValue: string
  ) => setSearchQuery(newInputValue);

  const handleOnChange = (
    event: React.SyntheticEvent,
    newValue: string | null
  ) => setValue(newValue);

  const getOptions = () => {
    if (!data) {
      return [];
    }
    // filter to remove duplicates and reduce information down
    return data?.results
      .filter(
        (curr: SearchResultProps, idx: number, arr: SearchResultProps[]) =>
          idx ===
          arr.findIndex(
            (t) =>
              t.query_result_headline_no_html ===
              curr.query_result_headline_no_html
          )
      )
      .map((result: SearchResultProps) => ({
        label: result.query_result_headline_no_html,
        render: result.query_result_headline,
      }));
  };

  const renderOption = (props: any, option: any) => {
    return (
      <ListItem disablePadding>
        <ListItemButton
          onClick={() => {
            setValue(option.label);
            navigate(`/search?q=${option.label}`);
            setOpen(false);
          }}
        >
          <div
            dangerouslySetInnerHTML={{
              __html: option.render,
            }}
          />
        </ListItemButton>
      </ListItem>
    );
  };

  const handleOnKeyDown: React.KeyboardEventHandler<HTMLDivElement> = (
    event
  ) => {
    if (event.key === "Enter") {
      navigate(`/search?q=${searchQuery}`);
    }
  };

  return (
    <Autocomplete
      id="navbar-search-box"
      open={open}
      onOpen={handleOnOpen}
      onClose={handleOnClose}
      size="small"
      onKeyDown={handleOnKeyDown}
      freeSolo
      value={value}
      autoComplete
      autoHighlight
      autoSelect
      onChange={handleOnChange}
      inputValue={searchQuery}
      onInputChange={handleOnInputChange}
      options={getOptions()}
      filterOptions={(x) => x}
      renderOption={renderOption}
      loading={isLoading}
      loadingText={<Loading />}
      renderInput={(params: any) => (
        <TextField
          {...params}
          onBlur={handleSearchOnBlur}
          autoFocus
          sx={{
            bgcolor:
              theme.palette.mode === "light"
                ? theme.palette.grey[200]
                : "default",
            borderRadius: 1,
          }}
          placeholder={"Search..."}
          InputProps={{
            ...params.InputProps,
            startAdornment: (
              <InputAdornment position="start">
                <IconButtonLink
                  to={`/search?q=${searchQuery}`}
                  onClick={() => setOpen(false)}
                >
                  <SearchIcon color="secondary" />
                </IconButtonLink>
              </InputAdornment>
            ),
          }}
        />
      )}
    />
  );
};

export default NavbarSearch;
