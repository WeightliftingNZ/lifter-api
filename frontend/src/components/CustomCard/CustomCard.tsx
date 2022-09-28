/** @format */

import React from "react";
import { Button, Card, CardContent, CardHeader } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import CardActionAreaLink from "../../components/CardActionAreaLink";
import { Box } from "@mui/system";
import { CustomCardProps } from "./interfaces";

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
          <Button size="large" color="secondary">
            See more
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default CustomCard;
