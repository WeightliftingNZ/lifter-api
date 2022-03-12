import React from "react";

const Navbar = () => {
  return (
    <div className="px-6 py-4 flex flex-rows border border-b-slate-400">
      <div className="basis-1/6">AppName</div>
      <div className="basis-4/6">Links</div>
      <div className="basis-1/6">Login/Logout</div>
    </div>
  );
};

export default Navbar;
