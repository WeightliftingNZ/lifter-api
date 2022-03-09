import React from "react";

const NavBar = () => {
  return (
    <div className="px-6 py-4 flex flex-rows border border-b-slate-400">
      <div className="basis-1/6">AppName</div>
      <div className="basis-4/6">Links</div>
      <div className="basis-1/6">Login/Logout</div>
    </div>
  );
};

function App() {
  return (
    <div className="grid grid-rows-1">
      <NavBar />
      <div className="px-12 py-4">
        <div className="card">
          <h1> Create you app </h1>
        </div>
      </div>
    </div>
  );
}

export default App;
