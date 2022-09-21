import React from "react";
import { Chip } from "@mui/material";
import { useTheme } from "@mui/material/styles";

const NationalsBadge: React.FC = () => {
  return <Chip label="Nationals" size="small" />;
};

const ClubBadge: React.FC = () => {
  return <Chip label="Club" size="small" />;
};

interface CompetitionBadgesProps {
  name: string;
}

const CompetitionBadges: React.FC<CompetitionBadgesProps> = ({ name }) => {
  const lowerName = name.toLowerCase();

  if (lowerName.includes("national")) {
    return <NationalsBadge />;
  } else if (lowerName.includes("club")) {
    return <ClubBadge />;
  }
  return null;
};

export default CompetitionBadges;
