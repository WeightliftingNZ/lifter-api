/** @format */

import React from "react";
import { TableContainer, Table, TableHead, TableBody } from "@mui/material";

interface NewCustomTableProps {
  headerRow: React.ReactNode;
  bodyRow: React.ReactNode;
}

const NewCustomTable: React.FC<NewCustomTableProps> = ({
  headerRow,
  bodyRow,
}) => {
  return (
    <TableContainer sx={{ overflowX: "scroll", maxWidth: "95vw" }}>
      <Table>
        <TableHead>{headerRow}</TableHead>
        <TableBody>{bodyRow}</TableBody>
      </Table>
    </TableContainer>
  );
};

export default NewCustomTable;
