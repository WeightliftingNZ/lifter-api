import React from "react";
import { Link } from "react-router-dom";

const Lost = () => {
  return (
    <>
      <div className="card">
        <h1>Are you lost?</h1>
        <p>
          <Link to="/">Navagate back to safety</Link>
        </p>
      </div>
    </>
  );
};

export default Lost;
