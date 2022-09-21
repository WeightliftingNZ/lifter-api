import React, { useEffect, useState, useRef, useCallback } from "react";
import { AthleteListObjectProps } from "../../interfaces";
import CustomSearchInput from "../../components/CustomSearchInput";
import { useDebounce } from "usehooks-ts";
import { useInfiniteQuery } from "react-query";
import AthleteCard from "./AthleteCard";
import { Stack, Box } from "@mui/material";
import apiClient from "../../utils/http-common";
import Title from "../../components/Title";
import SubTitle from "../../components/SubTitle";
import CustomError from "../../components/Error";
import CustomLoading from "../../components/Loading";

const PAGE_LIMIT = 10;

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

  console.dir(data?.pages[0].count);

  return (
    <>
      <Box>
        <Title>Athletes</Title>
        <SubTitle>Browse athletes</SubTitle>
      </Box>
      <Box sx={{ mt: 6 }}>
        <CustomSearchInput
          label="Search athletes"
          error={data?.pages[0].count === 0 ? true : false}
          placeholder="By first or last name"
          searchTerm={searchQuery}
          handleOnChange={handleOnChange}
        />
      </Box>
      <Box sx={{ mt: 6 }}>
        {isLoading && <CustomLoading />}
        {isError && <CustomError />}
        {isSuccess && (
          <>
            <Stack sx={{ maxWidth: "max-content" }} spacing={1}>
              {data?.pages.map((page) => (
                <>
                  {page.results.map((athlete: AthleteListObjectProps) => (
                    <AthleteCard
                      key={athlete.reference_id}
                      referenceId={athlete.reference_id}
                      fullName={athlete.full_name}
                      ageCategories={athlete.age_categories}
                      currentGrade={athlete.current_grade}
                      recentLift={athlete.recent_lift}
                    />
                  ))}
                </>
              ))}
            </Stack>
          </>
        )}
        <Box ref={observerElem}>
          {isFetchingNextPage && hasNextPage ? <CustomLoading /> : null}
        </Box>
      </Box>
    </>
  );
};

export default AthleteListPage;
