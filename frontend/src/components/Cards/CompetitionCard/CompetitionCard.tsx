/** @format */

import React from "react";
import { Divider } from "@mui/material";
import moment from "moment";
import { Box } from "@mui/system";
import CustomCard from "../CustomCard";
import CompetitionBadges from "../../CompetitionBadges";
import CompetitionCardTable from "./CompetitionCardTable";
import { CompetitionListObjectProps } from "../../../interfaces";
import NoResults from "../../NoResults";

const CompetitionCard: React.FC<CompetitionListObjectProps> = (competition) => {
  return (
    <CustomCard
      actionLink={`/competitions/${competition.reference_id}`}
      title={competition.name}
      subheader={
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            width: "fit-content",
            borderRadius: 1,
            color: "text.secondary",
            "& hr": {
              mx: 1,
            },
          }}
        >
          <Box>
            <CompetitionBadges name={competition.name} />
          </Box>
          <Box sx={{ display: "flex", flexDirection: "flex-start" }}>
            {moment(competition.date_start).fromNow()}
            <Divider orientation="vertical" variant="fullWidth" flexItem />
            {competition.lifts_count}{" "}
            {competition.lifts_count > 1 ? "athletes" : "athlete"}
          </Box>
        </Box>
      }
      contents={
        competition.best_lifts.length > 0 ? (
          <CompetitionCardTable {...competition} />
        ) : (
          <NoResults />
        )
      }
    />
  );
};

export default CompetitionCard;
