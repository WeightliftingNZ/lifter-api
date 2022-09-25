/** @format */

import React from "react";
import { Chip } from "@mui/material";
import { GradeT } from "../../interfaces";
import { useTheme } from "@mui/material/styles";

const EliteBadge: React.FC = () => {
  /* TODO: give tool tip for the weight category and standard */
  return <Chip label="Elite" size="small" />;
};

const InternationalBadge: React.FC = () => {
  const theme = useTheme();
  /* TODO: give tool tip for the weight category and standard */
  return (
    <Chip
      label="International"
      size="small"
      sx={{ backgroundColor: theme.palette.secondary.light }}
    />
  );
};

const AGradeBadge: React.FC = () => {
  /* TODO: give tool tip for the weight category and standard */
  return <Chip label="Grade A" size="small" />;
};

const BGradeBadge: React.FC = () => {
  /* TODO: give tool tip for the weight category and standard */
  return <Chip label="Grade B" size="small" />;
};

const CGradeBadge: React.FC = () => {
  /* TODO: give tool tip for the weight category and standard */
  return <Chip label="Grade C" size="small" />;
};

const DGradeBadge: React.FC = () => {
  /* TODO: give tool tip for the weight category and standard */
  return <Chip label="Grade D" size="small" />;
};

const EGradeBadge: React.FC = () => {
  /* TODO: give tool tip for the weight category and standard */
  return <Chip label="Grade E" size="small" />;
};

interface GradeProps {
  grade?: GradeT;
}

const GradeBadges: React.FC<GradeProps> = (props: GradeProps) => {
  const { grade } = props;
  switch (grade) {
    case "Elite":
      return <EliteBadge />;
    case "International":
      return <InternationalBadge />;
    case "A":
      return <AGradeBadge />;
    case "B":
      return <BGradeBadge />;
    case "C":
      return <CGradeBadge />;
    case "D":
      return <DGradeBadge />;
    case "E":
      return <EGradeBadge />;
    default:
      return <></>;
  }
};

export default GradeBadges;
