/** @format */

import { Box } from "@mui/system";
import { useInfiniteQuery } from "react-query";
import React, { useCallback, useRef, useEffect } from "react";
import apiClient from "../../utils/http-common/http-common";
import { CompetitionListObjectProps } from "../../interfaces";
import CustomError from "../../components/Error";
import CustomLoading from "../../components/Loading";
import CompetitionCard from "../../components/Cards/CompetitionCard";
import CompetitionRecentLoading from "./CompetitionRecentLoading";
import { PAGE_LIMIT } from "../../constants";
import NothingMore from "../../components/NothingMore";

const CompetitionRecent: React.FC = () => {
  const observerElem = useRef(null);

  const fetchRecentCompetitions = async (page: number) => {
    const res = await apiClient.get(
      `/competitions?page=${page}&page_size=${PAGE_LIMIT}`
    );
    return res.data;
  };

  const {
    data,
    error,
    isError,
    isLoading,
    isSuccess,
    hasNextPage,
    fetchNextPage,
    isFetchingNextPage,
  } = useInfiniteQuery(
    ["recentCompetitions"],
    ({ pageParam = 1 }) => fetchRecentCompetitions(pageParam),
    {
      enabled: true,
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
    <>
      <Box
        sx={{
          display: "flex",
          gap: 2,
          flexDirection: "column",
        }}
      >
        {isLoading && <CompetitionRecentLoading />}
        {isError && <CustomError />}
        {isSuccess && (
          <Box
            sx={{ display: "flex", flexDirection: "inherit", gap: "inherit" }}
          >
            {data?.pages.map((page) => (
              <React.Fragment key={page}>
                {page.results.map((competition: CompetitionListObjectProps) => (
                  <CompetitionCard
                    key={competition.reference_id}
                    {...competition}
                  />
                ))}
              </React.Fragment>
            ))}
          </Box>
        )}
      </Box>
      <Box id="infinity" ref={observerElem}>
        {isFetchingNextPage && hasNextPage && <CustomLoading />}
        {data?.pages[0].count > 0 && isSuccess && !hasNextPage && (
          <NothingMore />
        )}
      </Box>
    </>
  );
};

export default CompetitionRecent;
