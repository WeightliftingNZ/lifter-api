/** @format */

import React, { useEffect, useState, useRef, useCallback } from "react";
import { AthleteListObjectProps } from "../../interfaces";
import CustomSearchInput from "../../components/CustomSearchInput";
import { useDebounce } from "usehooks-ts";
import { useInfiniteQuery } from "react-query";
import AthleteCard from "../../components/Cards/AthleteCard";
import { Box } from "@mui/material";
import apiClient from "../../utils/http-common";
import Title from "../../components/Title";
import CustomError from "../../components/Error";
import CustomLoading from "../../components/Loading";
import { PAGE_LIMIT } from "../../constants";

const AthleteListPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const debouncedSearchQuery = useDebounce(searchQuery, 500);
  const observerElem = useRef(null);

  const fetchAthletes = async (page: number) => {
    const res = await apiClient.get(
      `/athletes?search=${debouncedSearchQuery}&page=${page}&page_size=${PAGE_LIMIT}`
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
    ["athletes", debouncedSearchQuery],
    ({ pageParam = 1 }) => fetchAthletes(pageParam),
    {
      enabled: debouncedSearchQuery ? true : false,
      getNextPageParam: (lastPage, pages) => {
        if (lastPage.next == null) {
          return undefined;
        }
        return pages.length + 1;
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

  const handleOnChange: React.ChangeEventHandler = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setSearchQuery(event.target.value);
  };

  return (
    <>
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          gap: 2,
        }}
      >
        <Box>
          <Box>
            <Title>Athlete Search</Title>
          </Box>
          <Box>
            <CustomSearchInput
              label="Search athletes"
              error={data?.pages[0].count === 0 ? true : false}
              placeholder="By first or last name"
              searchTerm={searchQuery}
              handleOnChange={handleOnChange}
            />
          </Box>
        </Box>
        <Box
          sx={{
            display: "flex",
            gap: "inherit",
            flexDirection: "inherit",
          }}
        >
          {isLoading && <CustomLoading />}
          {isError && <CustomError />}
          {isSuccess && (
            <Box
              sx={{ display: "flex", flexDirection: "inherit", gap: "inherit" }}
            >
              {data?.pages.map((page) => (
                <React.Fragment key={page}>
                  {page.results.map((athlete: AthleteListObjectProps) => (
                    <AthleteCard key={athlete.reference_id} {...athlete} />
                  ))}
                </React.Fragment>
              ))}
            </Box>
          )}
        </Box>
        <Box ref={observerElem}>
          {isFetchingNextPage && hasNextPage ? <CustomLoading /> : null}
        </Box>
      </Box>
    </>
  );
};

export default AthleteListPage;
