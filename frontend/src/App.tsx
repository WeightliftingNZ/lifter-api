import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import CompetitionListPage from "./views/CompetitionListPage";
import CompetitionDetailPage from "./views/CompetitionDetailPage";
import AthleteListPage from "./views/AthleteListPage";
import AthleteDetailPage from "./views/AthleteDetailPage";
import Box from "@mui/material/Box";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import { styled } from "@mui/material/styles";
import Home from "./views/Home";

const theme = createTheme({
  palette: {
    primary: {
      main: "#212121",
      light: "#484848",
      dark: "#000000",
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#78909c",
      light: "#a7c0cd",
      dark: "#4b636e",
      contrastText: "#000000",
    },
  },
});

const App: React.FC = () => {
  const NavbarHeader = styled("div")(({ theme }) => ({
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    padding: theme.spacing(0, 1),
    ...theme.mixins.toolbar,
  }));
  return (
    <>
      <ThemeProvider theme={theme}>
        <Box sx={{ display: "flex" }}>
          <Navbar />
          <Box
            component="main"
            sx={{ flexGrow: 1, p: 3, marginLeft: "auto", marginRight: "auto" }}
          >
            <NavbarHeader />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/competitions" element={<CompetitionListPage />} />
              <Route path="/athletes" element={<AthleteListPage />} />
              <Route
                path="/competitions/:competitionReferenceId"
                element={<CompetitionDetailPage />}
              />
              <Route
                path="/athletes/:athleteReferenceId"
                element={<AthleteDetailPage />}
              />
            </Routes>
          </Box>
        </Box>
      </ThemeProvider>
    </>
  );
};

export default App;
