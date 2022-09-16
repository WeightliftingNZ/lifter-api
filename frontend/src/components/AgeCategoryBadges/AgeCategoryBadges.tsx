import React from "react";
import { Chip, Stack } from "@mui/material";
import { AgeCategoriesProps } from "../../interfaces";
import { Tooltip } from "@mui/material";

const YouthBadge: React.FC = () => {
  return (
    <Tooltip title={<>Youth: Under 15</>}>
      <Chip label="Youth" size="small" />
    </Tooltip>
  );
};

const JuniorBadge: React.FC = () => {
  return (
    <Tooltip title={<>Junior: Under 20</>}>
      <Chip label="Junior" size="small" />
    </Tooltip>
  );
};

const SeniorBadge: React.FC = () => {
  return (
    <Tooltip title={<>Senior</>}>
      <Chip label="Senior" size="small" />
    </Tooltip>
  );
};

const MasterBadge: React.FC = () => {
  return (
    <Tooltip title={<>Masters: 35 and over</>}>
      <Chip label="Masters" size="small" />
    </Tooltip>
  );
};

interface AgeCategoryBadgesProps {
  ageCategories: AgeCategoriesProps;
}

const AgeCategoryBadges: React.FC<AgeCategoryBadgesProps> = (
  props: AgeCategoryBadgesProps
) => {
  const { ageCategories } = props;
  const { is_youth, is_junior, is_senior, is_master } = ageCategories;

  return (
    <Stack direction="row" spacing={1}>
      {is_youth ? <YouthBadge /> : <></>}
      {is_junior ? <JuniorBadge /> : <></>}
      {is_senior ? <SeniorBadge /> : <></>}
      {is_master ? <MasterBadge /> : <></>}
    </Stack>
  );
};

export default AgeCategoryBadges;
