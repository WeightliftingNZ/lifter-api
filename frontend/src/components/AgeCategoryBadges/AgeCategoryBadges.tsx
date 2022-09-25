/** @format */

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

const Master35to39Badge: React.FC = () => {
  return <Chip label="Masters 35-39" size="small" />;
};

const Master40to44Badge: React.FC = () => {
  return <Chip label="Masters 40-44" size="small" />;
};

const Master45to49Badge: React.FC = () => {
  return <Chip label="Masters 45-49" size="small" />;
};

const Master50to54Badge: React.FC = () => {
  return <Chip label="Masters 50-54" size="small" />;
};

const Master55to59Badge: React.FC = () => {
  return <Chip label="Masters 55-59" size="small" />;
};

const Master60to64Badge: React.FC = () => {
  return <Chip label="Masters 60-64" size="small" />;
};

const Master65to69Badge: React.FC = () => {
  return <Chip label="Masters 65-69" size="small" />;
};

const Master70Badge: React.FC = () => {
  return <Chip label="Masters 70+" size="small" />;
};

interface AgeCategoryBadgesProps {
  ageCategories: AgeCategoriesProps;
  isColumn?: boolean;
}

const AgeCategoryBadges: React.FC<AgeCategoryBadgesProps> = (
  props: AgeCategoryBadgesProps
) => {
  const { ageCategories, isColumn } = props;
  const {
    is_youth,
    is_junior,
    is_senior,
    is_master,
    is_master_35_39,
    is_master_40_44,
    is_master_45_49,
    is_master_50_54,
    is_master_55_59,
    is_master_60_64,
    is_master_65_69,
    is_master_70,
  } = ageCategories;

  return (
    <Stack direction={isColumn ? "column" : "row"} spacing={1}>
      {is_youth ? <YouthBadge /> : <></>}
      {is_junior ? <JuniorBadge /> : <></>}
      {is_senior ? <SeniorBadge /> : <></>}
      {is_master ? <MasterBadge /> : <></>}
      {is_master_35_39 ? <Master35to39Badge /> : <></>}
      {is_master_40_44 ? <Master40to44Badge /> : <></>}
      {is_master_45_49 ? <Master45to49Badge /> : <></>}
      {is_master_50_54 ? <Master50to54Badge /> : <></>}
      {is_master_55_59 ? <Master55to59Badge /> : <></>}
      {is_master_60_64 ? <Master60to64Badge /> : <></>}
      {is_master_65_69 ? <Master65to69Badge /> : <></>}
      {is_master_70 ? <Master70Badge /> : <></>}
    </Stack>
  );
};

export default AgeCategoryBadges;
