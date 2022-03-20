import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <div className="px-6 py-4 flex flex-rows border border-b-slate-400">
      <div className="basis-1/6">
        <Link to="/" className="hover:underline">
          Lifters
        </Link>
      </div>
      <div className="basis-4/6 flex gap-4">
        <Link to="/competitions/" className="hover:underline">
          Competitions
        </Link>
        <Link to="/athletes/" className="hover:underline">
          Athletes
        </Link>
      </div>
      <div className="basis-1/6"></div>
    </div>
  );
};

export default Navbar;
