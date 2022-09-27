/** @format */

import React from "react";
import Title from "../../components/Title";
import CompetitionRecent from "../CompetitionListPage/CompetitionRecent";

const Home: React.FC = () => {
  return (
    <>
      <Title>Recent Competitions</Title>
      <CompetitionRecent />
    </>
  );
};

export default Home;
