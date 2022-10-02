/** @format */

import React from "react";
import { Chip, Tooltip } from "@mui/material";
import { GradeT } from "../../interfaces";
import Body from "../Body";

interface BadgeProps {
  grade?: GradeT;
}

const GradeBadges: React.FC<BadgeProps> = ({ grade }) => {
  if (!grade) {
    return <></>;
  }

  const labelGrade = !(grade === "Elite" || grade === "International")
    ? `Grade ${grade}`
    : grade;

  return (
    <Tooltip
      title={
        <>
          <Body>{labelGrade}</Body>
          Required <em>N </em>kg total for <em>weight category</em>
          <br />
          Achieved: Coming soon
        </>
      }
    >
      <Chip sx={{ maxWidth: "fit-content" }} label={labelGrade} size="small" />
    </Tooltip>
  );
};

export default GradeBadges;
