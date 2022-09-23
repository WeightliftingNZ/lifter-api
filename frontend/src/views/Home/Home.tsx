import React from "react";
import Title from "../../components/Title";
import Body from "../../components/Body";
import Heading from "../../components/Heading";
import CompetitionFiveRecent from "../CompetitionListPage/CompetitionFiveRecent";
import { Box } from "@mui/system";

const Home: React.FC = () => {
  return (
    <>
      <Title>Welcome</Title>
      <Body>
        This is a database contain competitions for weightlifting results in New
        Zealand. We are in the process of adding results.
      </Body>
      <Heading>Recent Competitions</Heading>
      <Box
        sx={{
          display: "flex",
          flex: 1,
          gap: 2,
          flexDirection: "row",
          justifyContent: "flex-start",
          flexWrap: "wrap",
        }}
      >
        <CompetitionFiveRecent />
        {/* <Box> */}
        {/*   <Heading>Top Lifters</Heading> */}
        {/*   <Body>Coming soon ...</Body> */}
        {/* </Box> */}
      </Box>
    </>
  );
};

export default Home;
