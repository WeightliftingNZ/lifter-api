/** @format */

import React from "react";
import { Box } from "@mui/material";
import GradeBadges from "../../../components/GradeBadges";
import AgeCategoryBadges from "../../../components/AgeCategoryBadges";
import CustomCard from "../CustomCard";
import AthleteCardTable from "./AthleteCardTable";
import { AthleteListObjectProps } from "../../../interfaces";
import NoResults from "../../NoResults";

const AthleteCard: React.FC<AthleteListObjectProps> = (athlete) => {
  return (
    <CustomCard
      actionLink={`/athletes/${athlete.reference_id}`}
      title={athlete.full_name}
      subheader={
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            width: "fit-content",
            gap: 1,
            color: "text.secondary",
            "& hr": {
              mx: 1,
            },
          }}
        >
          <GradeBadges grade={athlete.current_grade} />
          <AgeCategoryBadges ageCategories={athlete.age_categories} />
        </Box>
      }
      contents={
        athlete.recent_lift.length > 0 ? (
          <AthleteCardTable {...athlete} />
        ) : (
          <NoResults />
        )
      }
    />
  );
};

export default AthleteCard;
