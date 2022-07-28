import React, { useEffect } from "react";
import { useInfiniteQuery } from "react-query";
import { Link } from "react-router-dom";
import { CompetitionObject } from "../../interfaces";
import { useInView } from "react-intersection-observer";
import apiClient from "../../utils/http-common";
import Loading from "../../components/Loading";
import Error from "../../components/Error";

const CompetitionsListPage = () => {
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
    "competitions",
    async ({ pageParam = 1 }) => {
      const res = await apiClient.get(`/competitions?page=${pageParam}`);
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
  return (
    <>
      {console.dir(data)}
      <div className="flex flex-col gap-2">
        {data?.pages[0].count === 0 ? (
          <div className="error-msg">There are no competitions.</div>
        ) : (
          data?.pages.map((group, idx) => (
            <div key={idx}>
              {group.results.map(
                (competition: CompetitionObject, idx: number) => (
                  <Link
                    key={idx}
                    to={`/competitions/${competition.reference_id}`}
                  >
                    <div className="card">
                      <h1>{competition.name}</h1>
                      <p>{competition.location}</p>
                      <p>{competition.date_start}</p>
                      <p>Sessions: {competition.lift_count}</p>
                    </div>
                  </Link>
                )
              )}
            </div>
          ))
        )}
      </div>
      <div>
        <button
          ref={ref}
          onClick={() => fetchNextPage()}
          disabled={!hasNextPage || isFetchingNextPage}
        >
          {isFetchingNextPage ? <Loading /> : "-"}
        </button>
        <div>{isFetching && !isFetchingNextPage ? <Loading /> : null}</div>
      </div>
    </>
  );
};

export default CompetitionsListPage;
