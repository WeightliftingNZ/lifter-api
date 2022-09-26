/** @format */

import React, { useState } from "react";
import { useDebounce } from "usehooks-ts";
import {
  Autocomplete,
  InputAdornment,
  LinearProgress,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Popper,
  PopperProps,
  Skeleton,
  TextField,
} from "@mui/material";
import { useQuery } from "react-query";
import apiClient from "../../utils/http-common/http-common";
import { useTheme } from "@mui/material/styles";
import SearchIcon from "@mui/icons-material/Search";
import SubTitle from "../SubTitle";
import Body from "../Body";
import { Box } from "@mui/system";

interface CustomPopperProps extends PopperProps {}

const CustomPopper = (props: CustomPopperProps) => {
  return <Popper {...props} placement="bottom" />;
};

interface CombinedSearchProps {
  handleSearchOnBlur: any;
}

/* TODO: types? */
const CombinedSearch: React.FC<CombinedSearchProps> = ({
  handleSearchOnBlur,
}) => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const debouncedSearchQuery = useDebounce(searchQuery, 500);
  const theme = useTheme();

  const fetchSearchResults = async () => {
    const PAGE_LIMIT = 10;
    const res = await apiClient.get(
      `/search?q=${debouncedSearchQuery}&page_limit=${PAGE_LIMIT}`
    );
    return res.data;
  };

  const handleOnChange = (event: React.SyntheticEvent, value: string) => {
    setSearchQuery(value);
  };

  const { data, error, isLoading, isError } = useQuery(
    ["search", debouncedSearchQuery],
    () => fetchSearchResults(),
    { enabled: debouncedSearchQuery ? true : false }
  );

  if (isError) {
    console.log(error);
  }

  const getOptions = () => {
    if (!data) {
      return [];
    }
    return data?.results;
  };

  const getOptionLabels = (option: any) => {
    return `${option?.query_result_headline_no_html}`;
  };

  const renderOption = (props: any, option: any) => {
    console.log("render", option);
    return (
      <List>
        <ListItem disablePadding>
          <ListItemButton>
            <ListItemText
              primary={
                <Body>
                  <div
                    dangerouslySetInnerHTML={{
                      __html: option?.query_result_headline,
                    }}
                  />
                </Body>
              }
            />
            <SubTitle>{option?.query_result_type}</SubTitle>
          </ListItemButton>
        </ListItem>
      </List>
    );
  };

  return (
    <Autocomplete
      id="search-box"
      freeSolo
      PopperComponent={CustomPopper}
      onInputChange={handleOnChange}
      options={getOptions()}
      getOptionLabel={getOptionLabels}
      filterOptions={(x) => x}
      loading={isLoading}
      loadingText={
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            gap: 4,
            justifySelf: "auto",
          }}
        >
          <>
            <LinearProgress color="secondary" />
            {Array.from(Array(4).keys()).map((idx: number) => {
              return (
                <Box
                  key={idx}
                  sx={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Skeleton sx={{ flexGrow: 4 }} animation="wave" />
                  <Box sx={{ flexGrow: 1 }} />
                  <Skeleton sx={{ flexGrow: 4 }} animation="wave" />
                  <Box sx={{ flexGrow: 3 }} />
                  <Skeleton sx={{ flexGrow: 2 }} animation="wave" />
                </Box>
              );
            })}
          </>
        </Box>
      }
      renderOption={renderOption}
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
          placeholder={"Search Competitions/Athletes"}
          InputProps={{
            ...params.InputProps,
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon color="secondary" />
              </InputAdornment>
            ),
          }}
        />
      )}
    />
  );
};

export default CombinedSearch;
