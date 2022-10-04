/** @format */

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import moment from "moment";
import { LiftObjectProps } from "../../../interfaces";
import LiftCells from "../../LiftCells";

const LiftCardTable: React.FC<LiftObjectProps> = (lift) => {
  return (
    <TableContainer sx={{ overflowX: "auto", maxWidth: "95vw" }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell colSpan={4}></TableCell>
            <TableCell align="center" colSpan={3}>
              Snatch
            </TableCell>
            <TableCell align="center" colSpan={3}>
              Clean and Jerk
            </TableCell>
            <TableCell align="center">Total</TableCell>
            <TableCell align="center">Sinclair</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow hover key={lift.reference_id}>
            <TableCell>{lift.placing}</TableCell>
            <TableCell sx={{ maxWidth: 100 }}>
              {moment(lift.competition_date_start).fromNow()}
            </TableCell>
            <TableCell
              sx={{
                overflow: "hidden",
                textOverflow: "ellipsis",
                maxWidth: 100,
              }}
            >
              {lift.team}
            </TableCell>
            <TableCell>{lift.weight_category}</TableCell>
            <LiftCells {...lift} />
            <TableCell align="center" sx={{ fontWeight: "bold" }}>
              {lift.total_lifted === 0 ? "-" : lift.total_lifted}
            </TableCell>
            <TableCell align="center">
              {lift.sinclair === 0 ? "-" : lift.sinclair}
            </TableCell>
          </TableRow>
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default LiftCardTable;
