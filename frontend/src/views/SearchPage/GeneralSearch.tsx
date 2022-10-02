/** @format */

import { Box } from "@mui/system";
import React, { useCallback, useEffect, useRef } from "react";
import { useInfiniteQuery } from "react-query";
import { useSearchParams } from "react-router-dom";
import AthleteCard from "../../components/Cards/AthleteCard";
import CompetitionCard from "../../components/Cards/CompetitionCard";
import LiftCard from "../../components/Cards/LiftCard";
import { PAGE_LIMIT } from "../../constants";
import { SearchResultProps } from "../../interfaces";
import apiClient from "../../utils/http-common/http-common";
import Error from "../../components/Error";
import { Alert } from "@mui/material";
import Loading from "../../components/Loading";

interface SearchCardResultProps {
  result: SearchResultProps;
}

const SearchCardResult: React.FC<SearchCardResultProps> = ({ result }) => {
  switch (result.query_result_type) {
    case "Athlete":
      return <AthleteCard {...result.query_result} />;
    case "Competition":
      return <CompetitionCard {...result.query_result} />;
    case "Lift":
      return <LiftCard {...result.query_result} />;
    default:
      return <></>;
  }
};

const GeneralSearch: React.FC = () => {
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
    ["search", searchQuery],
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

  console.log(data);

  return (
    <>
      <Box
        sx={{
          display: "flex",
          gap: 2,
          flexDirection: "column",
        }}
      >
        <>
          {isError && <Error />}
          {isLoading && <Loading />}
          {isSuccess &&
            data &&
            (data?.pages[0].count > 0 ? (
              data?.pages.map((page) => {
                return (
                  <React.Fragment key={page}>
                    {page.results.map((result: SearchResultProps) => (
                      <SearchCardResult
                        key={result.query_result.reference_id}
                        result={result}
                      />
                    ))}
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
    </>
  );
};

export default GeneralSearch;
