/** @format */

import React, { useRef, useState, useCallback, useEffect } from "react";
import CustomSearchInput from "../../components/CustomSearchInput";
import apiClient from "../../utils/http-common/http-common";
import { CompetitionListObjectProps } from "../../interfaces";
import Title from "../../components/Title";
import { useDebounce } from "usehooks-ts";
import CompetitionCard from "../../components/CompetitionCard";
import { Stack, Box, TextField } from "@mui/material";
import { useInfiniteQuery } from "react-query";
import CustomError from "../../components/Error";
import CustomLoading from "../../components/Loading";
import { MobileDatePicker } from "@mui/x-date-pickers/MobileDatePicker";
import moment from "moment";
import { PAGE_LIMIT } from "../../constants";

const CompetitionListPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [dateAfter, setDateAfter] = useState<string | null>(null);
  const [dateBefore, setDateBefore] = useState<string | null>(null);
  const debouncedSearchQuery = useDebounce<string>(searchQuery, 500);
  const observerElem = useRef(null);

  const fetchCompetitions = async (page: number) => {
    const res = await apiClient.get(
      `/competitions?search=${debouncedSearchQuery}&date_start_after=${
        dateAfter ? moment(dateAfter).format("YYYY-MM-DD") : ""
      }&date_start_before=${
        dateBefore ? moment(dateBefore).format("YYYY-MM-DD") : ""
      }&page=${page}&page_size=${PAGE_LIMIT}`
    );
    return res.data;
  };

  const {
    data,
    error,
    isLoading,
    isError,
    isSuccess,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery(
    ["competitions", debouncedSearchQuery, dateBefore, dateAfter],
    ({ pageParam = 1 }) => fetchCompetitions(pageParam),
    {
      enabled: debouncedSearchQuery || dateBefore || dateAfter ? true : false,
      getNextPageParam: (lastPage, page) => {
        if (lastPage.next == null) {
          return undefined;
        }
        return page.length + 1;
      },
    }
  );

  const handleObserver: IntersectionObserverCallback = useCallback(
    (entries) => {
      const [target] = entries;
      if (target.isIntersecting && hasNextPage) {
        fetchNextPage();
      }
    },
    [fetchNextPage, hasNextPage]
  );

  useEffect(() => {
    const element = observerElem.current;
    const option = { threshold: 0 };

    const observer = new IntersectionObserver(handleObserver, option);
    observer.observe(element!);
    return () => observer.unobserve(element!);
  }, [fetchNextPage, hasNextPage, handleObserver]);

  if (isError) {
    console.log(error);
  }

  const handleOnChangeSearchInput: React.ChangeEventHandler = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setSearchQuery(event.target.value);
  };

  const handleOnChangeDateAfterInput = (newValue: string | null) => {
    setDateAfter(moment(newValue).startOf("month").format("YYYY-MM-DD"));
  };

  const handleOnChangeDateBeforeInput = (newValue: string | null) => {
    setDateBefore(moment(newValue).endOf("month").format("YYYY-MM-DD"));
  };

  return (
    <Box
      sx={{
        display: "flex",
        flexWrap: "wrap",
        gap: 2,
        justifyContent: "flex-start",
      }}
    >
      <Box>
        <Box>
          <Title>Competition Search</Title>
        </Box>
        <Stack spacing={2}>
          <CustomSearchInput
            label="Search competitions"
            error={data?.pages[0].count === 0 ? true : false}
            placeholder="By name and/or location"
            searchTerm={searchQuery}
            handleOnChange={handleOnChangeSearchInput}
          />
          <Stack direction="row" spacing={2}>
            <MobileDatePicker
              views={["year", "month"]}
              openTo="year"
              label="Date After"
              value={dateAfter}
              disableFuture
              onChange={handleOnChangeDateAfterInput}
              renderInput={(params) => <TextField {...params} />}
            />
            <MobileDatePicker
              views={["year", "month"]}
              label="Date Before"
              value={dateBefore}
              openTo="year"
              disableFuture
              onChange={handleOnChangeDateBeforeInput}
              renderInput={(params) => <TextField {...params} />}
            />
          </Stack>
        </Stack>
      </Box>
      <Box
        sx={{
          display: "flex",
          flex: 1,
          gap: 0,
          flexDirection: "column",
          alignItems: "flex-start",
        }}
      >
        {isLoading && <CustomLoading />}
        {isError && <CustomError />}
        {isSuccess && (
          <Stack sx={{ maxWidth: "max-content", minWidth: "40%" }} spacing={1}>
            {data?.pages.map((page) => (
              <React.Fragment key={page}>
                {page.results.map((competition: CompetitionListObjectProps) => (
                  <CompetitionCard
                    key={competition.reference_id}
                    referenceId={competition.reference_id}
                    name={competition.name}
                    location={competition.location}
                    dateStart={competition.date_start}
                    dateEnd={competition.date_end}
                    liftCount={competition.lifts_count}
                    randomLifts={competition.random_lifts}
                  />
                ))}
              </React.Fragment>
            ))}
          </Stack>
        )}
        <Box ref={observerElem}>
          {isFetchingNextPage && hasNextPage ? <CustomLoading /> : null}
        </Box>
      </Box>
    </Box>
  );
};

export default CompetitionListPage;
