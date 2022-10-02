/** @format */

import React from "react";
import { Box, Card, CardContent, CardHeader } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import CardActionAreaLink from "../CardActionAreaLink";
import { CustomCardProps } from "./interfaces";
import ButtonLink from "../../ButtonLink";

const CustomCard: React.FC<CustomCardProps> = ({
  actionLink,
  title,
  subheader,
  contents,
}) => {
  const theme = useTheme();
  return (
    <Card
      variant="outlined"
      elevation={0}
      sx={{
        maxWidth: "100vw",
        "&:hover": {
          borderColor: theme.palette.secondary.light,
          boxShadow: 2,
        },
      }}
    >
      <CardActionAreaLink to={actionLink || ""}>
        <CardHeader title={title} subheader={subheader} />
      </CardActionAreaLink>
      <CardContent>
        {contents}
        <Box sx={{ display: "flex", justifyContent: "flex-end" }}>
          {/* <Button size="large" color="secondary"> */}
          {/*   Share */}
          {/* </Button> */}
          <ButtonLink to={actionLink} size="large" color="secondary">
            See more
          </ButtonLink>
        </Box>
      </CardContent>
    </Card>
  );
};

export default CustomCard;
