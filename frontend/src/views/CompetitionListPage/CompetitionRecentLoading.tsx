/** @format */

import React from "react";
import CustomLoading from "../../components/Loading";

const CompetitionRecentLoading: React.FC = () => {
  const NUM = 4;
  return (
    <>
      {Array.from(Array(NUM).keys()).map((idx: number) => {
        return (
          <React.Fragment key={idx}>
            <CustomLoading />
          </React.Fragment>
        );
      })}
    </>
  );
};

export default CompetitionRecentLoading;
