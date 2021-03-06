import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./views/HomePage";
import CompetitionsListPage from "./views/CompetitionsListPage";
import CompetitionDetailPage from "./views/CompetitionDetailPage/CompetitionDetailPage"; // TODO: fix this barrel
import AthletesListPage from "./views/AthletesListPage";
import AthleteDetailPage from "./views/AthleteDetailPage";
import Lost from "./components/Lost";

function App() {
  return (
    <div className="grid grid-rows-1">
      <Navbar />
      <div className="px-6 py-4 flex flex-col gap-2 justify-center items-center min-w-full">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route
            path="/competitions"
            element={<CompetitionsListPage />}
          ></Route>
          <Route
            path="/competitions/:competitionReferenceId"
            element={<CompetitionDetailPage />}
          />
          <Route
            path="/competitions/:competitionReferenceId/sessions/:sessionReferenceId"
            element={<CompetitionDetailPage />}
          />
          <Route path="/athletes" element={<AthletesListPage />}></Route>
          <Route
            path="/athletes/:athleteReferenceId"
            element={<AthleteDetailPage />}
          ></Route>
          <Route
            path="*"
            element={
              <>
                <Lost />
              </>
            }
          />
        </Routes>
      </div>
    </div>
  );
}

export default App;
