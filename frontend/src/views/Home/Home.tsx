/** @format */

import React from "react";
import Heading from "../../components/Heading";
import CompetitionRecent from "../CompetitionListPage/CompetitionRecent";

const Home: React.FC = () => {
  return (
    <>
      <Heading>Recent Competitions</Heading>
      <CompetitionRecent />
    </>
  );
};

export default Home;
