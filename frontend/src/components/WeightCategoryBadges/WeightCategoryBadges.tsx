import React from "react";
import { Chip } from "@mui/material";

interface WeightCategoryBadgeProps {
  weightCategory: string;
}

const WeightCategoryBadge: React.FC<WeightCategoryBadgeProps> = (
  props: WeightCategoryBadgeProps
) => {
  const { weightCategory } = props;

  return (
    <Chip
      label={weightCategory.replace("W", "Women's ").replace("M", "Men's ")}
      size="small"
    />
  );
};

export default WeightCategoryBadge;
