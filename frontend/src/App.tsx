/** @format */

import React, { useMemo, createContext, useState } from "react";
import { Routes, Route } from "react-router-dom";
import CompetitionListPage from "./views/CompetitionListPage";
import CompetitionDetailPage from "./views/CompetitionDetailPage";
import AthleteListPage from "./views/AthleteListPage";
import AthleteDetailPage from "./views/AthleteDetailPage";
import SearchPage from "./views/SearchPage";
import {
  ThemeProvider,
  createTheme,
  responsiveFontSizes,
} from "@mui/material/styles";
import Home from "./views/Home";
import Navbar from "./components/Navbar";
import { useMediaQuery } from "@mui/material";
import { AdapterMoment } from "@mui/x-date-pickers/AdapterMoment";
import { LocalizationProvider } from "@mui/x-date-pickers";
import type {} from "@mui/x-date-pickers/themeAugmentation";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import NotFound from "./views/NotFound";

export const ColorModeContext = createContext({ toggleColorMode: () => {} });

const App: React.FC = () => {
  const prefersDarkmode = useMediaQuery("(prefers-color-scheme: dark)");
  const [darkmode, setDarkMode] = useState<boolean>(prefersDarkmode === true);
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setDarkMode((prevMode) => !prevMode);
      },
    }),
    []
  );
  const mode = darkmode ? "dark" : "light";
  let theme = useMemo(
    () =>
      createTheme({
        typography: {
          fontFamily: "Roboto",
        },
        palette: {
          mode,
          primary: {
            main: "#424242",
            light: "#1b1b1b",
            dark: "#000000",
            contrastText: "#FFFFFF",
          },
          secondary: {
            main: "#b0bec5",
            light: "#e21f8",
            dark: "#808e95",
            contrastText: "#FFFFFF",
          },
        },
        components: {
          MuiDatePicker: {
            styleOverrides: {
              root: {
                backgroundColor: "red",
              },
            },
          },
        },
      }),
    [mode]
  );
  theme = responsiveFontSizes(theme);

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <LocalizationProvider dateAdapter={AdapterMoment}>
          <Navbar>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/competitions" element={<CompetitionListPage />} />
              <Route path="/athletes" element={<AthleteListPage />} />
              <Route
                path="/competitions/:competitionReferenceId"
                element={<CompetitionDetailPage />}
              />
              <Route
                path="/athletes/:athleteReferenceId/*"
                element={<AthleteDetailPage />}
              />
              <Route path="/search" element={<SearchPage />} />
              <Route path="/*" element={<NotFound />} />
            </Routes>
          </Navbar>
        </LocalizationProvider>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
};

export default App;
