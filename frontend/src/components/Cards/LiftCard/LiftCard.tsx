/** @format */

import React from "react";
import { Box } from "@mui/material";
import CustomCard from "../CustomCard";
import LiftCardTable from "./LiftCardTable";
import { LiftObjectProps } from "../../../interfaces";

const LiftCard: React.FC<LiftObjectProps> = (lift) => {
  return (
    <CustomCard
      actionLink={`/competitions/${lift.competition}`}
      title={`Lift from ${lift.competition_name}`}
      subheader={
        <Box
          sx={{
            display: "flex",
            alignItems: "center",
            width: "fit-content",
            borderRadius: 1,
            "& hr": {
              mx: 1,
            },
          }}
        >
          {lift.athlete_name}
        </Box>
      }
      contents={<LiftCardTable {...lift} />}
    />
  );
};

export default LiftCard;
