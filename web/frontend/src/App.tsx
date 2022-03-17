import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./views/HomePage";
import CompetitionsListPage from "./views/CompetitionsListPage";
import CompetitionDetailPage from "./views/CompetitionDetailPage/CompetitionDetailPage"; // TODO: fix this barrel

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
            path="*"
            element={
              <>
                <div className="card">Whoops!</div>
              </>
            }
          />
        </Routes>
      </div>
    </div>
  );
}

export default App;
