/** @format */

import React, { useCallback, useEffect, useRef } from "react";
import { useInfiniteQuery } from "react-query";
import Title from "../../components/Title";
import AthleteCard from "../../components/Cards/AthleteCard";
import CompetitionCard from "../../components/Cards/CompetitionCard";
import LiftCard from "../../components/Cards/LiftCard";
import { Box } from "@mui/material";
import { useSearchParams } from "react-router-dom";
import apiClient from "../../utils/http-common/http-common";
import Error from "../../components/Error";
import { PAGE_LIMIT } from "../../constants";
import Loading from "../../components/Loading";
import { Alert } from "@mui/material";
import { SearchResultProps } from "../../interfaces";

const SearchPage: React.FC = () => {
  const [searchQuery] = useSearchParams();
  const observerElem = useRef(null);

  const fetchSearchResults = async (page: number) => {
    const res = await apiClient.get(
      `/search?${searchQuery}&page=${page}&page_size=${PAGE_LIMIT}`
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
    ["searchPage", searchQuery.get("q")],
    ({ pageParam = 1 }) => fetchSearchResults(pageParam),
    {
      enabled: searchQuery ? true : false,
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
        Search: {searchQuery.get("q")}
      </Title>
      <Box>
        <>
          {isError && <Error />}
          {isLoading && <Loading />}
          {isSuccess &&
            data &&
            (data?.pages[0].count > 0 ? (
              data?.pages.map((page) => {
                return (
                  <React.Fragment key={page}>
                    {page.results.map((result: SearchResultProps) => {
                      switch (result.query_result_type) {
                        case "Athlete":
                          return (
                            <AthleteCard
                              key={result.query_result.reference_id}
                              {...result.query_result}
                            />
                          );
                        case "Competition":
                          return (
                            <CompetitionCard
                              key={result.query_result.reference_id}
                              {...result.query_result}
                            />
                          );
                        case "Lift":
                          return (
                            <LiftCard
                              key={result.query_result.reference_id}
                              {...result.query_result}
                            />
                          );
                        default:
                          return <></>;
                      }
                    })}
                  </React.Fragment>
                );
              })
            ) : (
              <Box>No results.</Box>
            ))}
        </>
      </Box>
      <Box id="infinity" ref={observerElem}>
        {isFetchingNextPage && hasNextPage && <Loading />}
        {data?.pages[0].count > 0 && isSuccess && !hasNextPage && (
          <Alert sx={{ m: 2 }} severity="success">
            Nothing more to show!
          </Alert>
        )}
      </Box>
    </Box>
  );
};

export default SearchPage;
