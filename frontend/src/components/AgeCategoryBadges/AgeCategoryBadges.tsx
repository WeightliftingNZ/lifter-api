import React from "react";
import { Chip, Stack } from "@mui/material";
import { AgeCategoriesProps } from "../../interfaces";

const YouthBadge: React.FC = () => {
  return <Chip label="Youth" size="small" />;
};

const JuniorBadge: React.FC = () => {
  return <Chip label="Junior" size="small" />;
};

const SeniorBadge: React.FC = () => {
  return <Chip label="Senior" size="small" />;
};

const MasterBadge: React.FC = () => {
  return <Chip label="Masters" size="small" />;
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
