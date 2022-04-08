import React, { useState, useEffect } from "react";
import { useInfiniteQuery } from "react-query";
import { Link } from "react-router-dom";
import { useDebounce } from "usehooks-ts";
import { useInView } from "react-intersection-observer";
import apiClient from "../../utils/http-common";
import Error from "../../components/Error";
import Loading from "../../components/Loading";
import { AthleteObject } from "../../interfaces";

// search using API filter
const SearchOutput = (debouncedSearchQuery: any) => {
  const { ref, inView } = useInView();

  const {
    data,
    error,
    isLoading,
    isError,
    fetchNextPage,
    hasNextPage,
    isFetching,
    isFetchingNextPage,
  } = useInfiniteQuery(
    ["athletesSearch", debouncedSearchQuery],
    async ({ pageParam = 1 }) => {
      const pageSearch = pageParam === 1 ? "" : `page=${pageParam}&`;
      const res = await apiClient.get(
        `/athletes?${pageSearch}search=${debouncedSearchQuery.updateSearchQuery}`
      );
      return res.data;
    },
    {
      getNextPageParam: (lastPage, pages) => {
        if (lastPage.next == null) {
          return undefined;
        }
        return pages.length + 1;
      },
    }
  );

  useEffect(() => {
    if (inView) {
      fetchNextPage();
    }
  }, [inView]);

  if (isLoading) {
    return (
      <>
        <Loading />
      </>
    );
  }
  if (isError) {
    console.log(error);
    return (
      <>
        <Error />
      </>
    );
  }

  if (debouncedSearchQuery.updateSearchQuery === "") {
    return <></>;
  }

  return (
    <div className="flex flex-col gap-2">
      {data?.pages.map((group, idx) => (
        <div key={idx}>
          {group.results.map((athlete: AthleteObject, idx: number) => {
            return (
              <Link key={idx} to={`/athletes/${athlete.reference_id}`}>
                <div className="card">{athlete.full_name}</div>
              </Link>
            );
          })}
        </div>
      ))}
      <div>
        <button
          ref={ref}
          onClick={() => fetchNextPage()}
          disabled={!hasNextPage || isFetchingNextPage}
        >
          {isFetchingNextPage ? <Loading /> : "End"}
          <div>{isFetching && !isFetchingNextPage ? <Loading /> : null}</div>
        </button>
      </div>
    </div>
  );
};

const AthletesListPage = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const debouncedSearchQuery = useDebounce(searchQuery, 300);

  const handleChange = (e: any) => {
    if (e.target.value !== null) {
      setSearchQuery(e.target.value);
    }
  };

  const handleKeyPress = (e: any) => {
    if (e.keyCode === 13 && e.target.value !== null) {
      setSearchQuery(e.target.value);
    }
  };
  const handleClick = (e: any) => {
    if (e.target.value !== null) {
      setSearchQuery(e.target.value);
    }
  };
  return (
    <>
      <div className="flex">
        <input
          onChange={handleChange}
          onKeyPress={handleKeyPress}
          id="athlete_search"
          placeholder="Search Athlete"
        />
        <button className="btn rounded-xl" onClick={handleClick}>
          <svg
            focusable="false"
            data-prefix="fas"
            data-icon="search"
            className="pl-1 w-4"
            role="img"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 512 512"
          >
            <path
              fill="currentColor"
              d="M505 442.7L405.3 343c-4.5-4.5-10.6-7-17-7H372c27.6-35.3 44-79.7 44-128C416 93.1 322.9 0 208 0S0 93.1 0 208s93.1 208 208 208c48.3 0 92.7-16.4 128-44v16.3c0 6.4 2.5 12.5 7 17l99.7 99.7c9.4 9.4 24.6 9.4 33.9 0l28.3-28.3c9.4-9.4 9.4-24.6.1-34zM208 336c-70.7 0-128-57.2-128-128 0-70.7 57.2-128 128-128 70.7 0 128 57.2 128 128 0 70.7-57.2 128-128 128z"
            ></path>
          </svg>
        </button>
      </div>
      <div>
        <SearchOutput updateSearchQuery={debouncedSearchQuery} />
      </div>
    </>
  );
};

export default AthletesListPage;
