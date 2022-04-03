import React, { useState } from "react";
import { useQuery } from "react-query";
import { Link } from "react-router-dom";
import { useDebounce } from "usehooks-ts";
import apiClient from "../../utils/http-common";

// search using API filter
const SearchOutput = (debouncedSearchQuery: any) => {
  const [searchResult, setSearchResult] = useState({
    count: 0,
    next: "",
    previous: "",
    results: [
      {
        reference_id: "",
        full_name: "",
        first_name: "",
        last_name: "",
        yearborn: "",
      },
    ],
  });

  const { isLoading, isError } = useQuery(
    ["athletesSearch", debouncedSearchQuery],
    async () => {
      return await apiClient.get(
        `/athletes?search=${debouncedSearchQuery.updateSearchQuery}`
      );
    },
    {
      enabled: Boolean(debouncedSearchQuery.updateSearchQuery),
      onSuccess: (res) => {
        const result = {
          status: res.status + "-" + res.statusText,
          headers: res.headers,
          data: res.data,
        };
        setSearchResult(result.data);
      },
      onError: (err) => {
        console.log(err);
      },
    }
  );

  if (isLoading) {
    return (
      <>
        <p>Loading...</p>
      </>
    );
  }
  if (isError) {
    return (
      <>
        <p>Error!!</p>
      </>
    );
  }
  const athletes = searchResult.results;

  if (debouncedSearchQuery.updateSearchQuery === "") {
    return <></>;
  }

  if (searchResult.results.length === 0) {
    return (
      <p className="text-red-400">
        No Athlete named &quot;{debouncedSearchQuery.updateSearchQuery}&quot;
        found.
      </p>
    );
  }

  return (
    <div className="flex flex-col gap-2">
      {athletes.map((athlete, idx) => {
        return (
          <Link
            key={idx}
            className="card"
            to={`/athletes/${athlete.reference_id}`}
          >
            {athlete.full_name}
          </Link>
        );
      })}
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
