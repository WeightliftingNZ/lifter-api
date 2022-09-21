import React from "react";
import Title from "../../components/Title";
import Body from "../../components/Body";
import Heading from "../../components/Heading";
import CompetitionFiveRecent from "../CompetitionListPage/CompetitionFiveRecent";

const Home: React.FC = () => {
  return (
    <>
      <Title>Welcome</Title>
      <Body>
        This is a database contain competitions for weightlifting results in New
        Zealand. We are in the process of adding results.
      </Body>
      <Heading>Recent Competitions</Heading>
      <CompetitionFiveRecent />
      <Heading>Top Lifters</Heading>
      <Body>Coming soon ...</Body>
    </>
  );
};

export default Home;
