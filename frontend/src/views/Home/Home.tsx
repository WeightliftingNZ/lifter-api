import React from "react";
import Title from "../../components/Title";
import Body from "../../components/Body";

const Home: React.FC = () => {
  return (
    <>
      <Title>Welcome</Title>
      <Body>
        This is a database contain competitions for weightlifting results in New
        Zealand. We are in the process of adding results.
      </Body>
      <Title>Recent Competitions</Title>
      <Body>Coming soon ...</Body>
      <Title>Top Lifters</Title>
      <Body>Coming soon ...</Body>
    </>
  );
};

export default Home;
