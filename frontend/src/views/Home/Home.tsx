import React from "react";
import Typography from "@mui/material/Typography";

const Home: React.FC = () => {
  return (
    <>
      <Typography variant="h4">Welcome</Typography>
      <Typography variant="body1">
        This is a database contain competitions for weightlifting results in New
        Zealand. We are in the process of adding results.
      </Typography>
    </>
  );
};

export default Home;
