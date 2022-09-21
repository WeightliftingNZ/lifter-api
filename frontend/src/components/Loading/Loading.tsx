import React from "react";
import {
  Stack,
  Card,
  Box,
  Skeleton,
  CardContent,
  Table,
  TableHead,
  TableRow,
  TableCell,
} from "@mui/material";
import Heading from "../Heading";

const Loading: React.FC = () => {
  return (
    <Box sx={{ width: "50%" }}>
      <Card variant="outlined" elevation={2}>
        <CardContent>
          <Box>
            <Heading>
              <Skeleton sx={{ width: "40%" }} />
            </Heading>
            <Stack direction="row" spacing={1}>
              <Skeleton sx={{ width: "8%" }} />
              <Skeleton sx={{ width: "8%" }} />
            </Stack>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>
                    <Skeleton />
                  </TableCell>
                  <TableCell>
                    <Skeleton />
                  </TableCell>
                  <TableCell>
                    <Skeleton />
                  </TableCell>
                </TableRow>
                <TableRow>
                  <TableCell>
                    <Skeleton />
                  </TableCell>
                  <TableCell>
                    <Skeleton />
                  </TableCell>
                  <TableCell>
                    <Skeleton />
                  </TableCell>
                </TableRow>
              </TableHead>
            </Table>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default Loading;
