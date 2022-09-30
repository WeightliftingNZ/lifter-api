/** @format */

import React from "react";
import Title from "../../components/Title";
import {
  Box,
  IconButton,
  Skeleton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import Body from "../../components/Body";
import { KeyboardArrowUp } from "@mui/icons-material";

const LoadingTable: React.FC = () => (
  <TableContainer sx={{ maxWidth: "95vw" }}>
    <Table>
      <TableHead>
        <TableRow>
          <TableCell>
            <Box sx={{ display: "flex", alignItems: "center" }}>
              <Body>
                <Skeleton width={100} />
              </Body>
              <IconButton>
                <KeyboardArrowUp />
              </IconButton>
            </Box>
          </TableCell>
          <TableCell colSpan={3}></TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        <TableRow>
          <TableCell>
            <TableContainer>
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
            </TableContainer>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </TableContainer>
);

const CustomLoading: React.FC = () => {
  const NUM = 3;
  return (
    <Box sx={{ m: 1 }}>
      <Title>
        <Skeleton width={400} />
        <Skeleton width={250} />
      </Title>
      <Box sx={{ display: "flex", gap: 1 }}>
        <Box>
          <Body>
            <Skeleton width={100} />
          </Body>
          <Body>
            <Skeleton width={100} />
          </Body>
        </Box>
        <Box>
          <Body>
            <Skeleton width={100} />
          </Body>
          <Body>
            <Skeleton width={100} />
          </Body>
        </Box>
      </Box>
      {Array.from(Array(NUM).keys()).map((idx: number) => {
        return (
          <React.Fragment key={idx}>
            <LoadingTable />
          </React.Fragment>
        );
      })}
    </Box>
  );
};

export default CustomLoading;
