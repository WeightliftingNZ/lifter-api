import React from "react";
import { Typography } from "@mui/material";
import Title from "../../components/Title";

const Home: React.FC = () => {
  return (
    <>
      <Title>Welcome</Title>
      <Typography variant="body1">
        This is a database contain competitions for weightlifting results in New
        Zealand. We are in the process of adding results.
      </Typography>
    </>
  );
};

export default Home;
