import React from "react";
import apiClient from "../../utils/http-common/http-common";
import CompetitionsListPage from "../CompetitionsListPage";

const HomePage = () => {
  console.dir(apiClient.defaults.baseURL);

  return (
    <>
      <h2>Welcome to Lifter</h2>
      <a href={apiClient.defaults.baseURL}>
        The API can be located:{" "}
        <span className="text underline text-blue-600">
          {apiClient.defaults.baseURL}
        </span>
      </a>
      <h2>Recent Competitions:</h2>
      <CompetitionsListPage />
    </>
  );
};

export default HomePage;
