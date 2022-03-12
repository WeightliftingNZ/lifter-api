import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./views/HomePage";
import CompetitionsListPage from "./views/CompetitionsListPage";

function App() {
  return (
    <div className="grid grid-rows-1">
      <Navbar />
      <div className="px-12 py-4 flex flex-col gap-2 min-w-full">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/competitions" element={<CompetitionsListPage />}>
            <Route
              path=":competitionReferenceId"
              element={<CompetitionsListPage />}
            />
          </Route>
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
