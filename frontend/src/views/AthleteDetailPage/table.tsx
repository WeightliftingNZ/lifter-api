import React from "react";
import { useMemo, forwardRef } from "react";
import Paper from "@mui/material/Paper";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
/* TODO: below is temporary */
import { StyledTableCell } from "../../components/CustomTable/customStyles";
/* TODO: above is temporary */
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";
import { useTheme } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import { red, green, grey } from "@mui/material/colors";
import { Column } from "./interfaces";

/* TODO refactor below code?  */
const isBestLift = (idx: number, column: Column, currentRow: any) => {
  let isBold = false; // if the lift is the best lift
  let currentLiftStatus = "";
  let value = currentRow[column.id];

  const bestSnatch = currentRow.best_snatch_weight[0];
  const bestCnj = currentRow.best_cnj_weight[0];

  switch (column.id.replace("_weight", "")) {
    case "snatch_first":
      if (bestSnatch === "1st") {
        isBold = true;
      }
      currentLiftStatus = currentRow.snatches["1st"].lift_status;
      if (currentLiftStatus === "DNA") {
        value = "-";
      }
      break;
    case "snatch_second":
      if (bestSnatch === "2nd") {
        isBold = true;
      }
      currentLiftStatus = currentRow.snatches["2nd"].lift_status;
      if (currentLiftStatus === "DNA") {
        value = "-";
      }
      break;
    case "snatch_third":
      if (bestSnatch === "3rd") {
        isBold = true;
      }
      currentLiftStatus = currentRow.snatches["3rd"].lift_status;
      if (currentLiftStatus === "DNA") {
        value = "-";
      }
      break;
    case "cnj_first":
      if (bestCnj === "1st") {
        isBold = true;
      }
      currentLiftStatus = currentRow.cnjs["1st"].lift_status;
      if (currentLiftStatus === "DNA") {
        value = "-";
      }
      break;
    case "cnj_second":
      if (bestCnj === "2nd") {
        isBold = true;
      }
      currentLiftStatus = currentRow.cnjs["2nd"].lift_status;
      if (currentLiftStatus === "DNA") {
        value = "-";
      }
      break;
    case "cnj_third":
      if (bestCnj === "3rd") {
        isBold = true;
      }
      currentLiftStatus = currentRow.cnjs["3rd"].lift_status;
      if (currentLiftStatus === "DNA") {
        value = "-";
        break;
      }
  }

  switch (currentLiftStatus) {
    case "LIFT":
      return (
        <StyledTableCell
          key={idx}
          align={column.align}
          sx={
            isBold
              ? {
                  backgroundColor: green[100],
                  borderWidth: 3,
                  borderColor: green[800],
                }
              : { backgroundColor: green[100], borderColor: green[800] }
          }
        >
          <Typography
            sx={
              isBold
                ? { fontWeight: "bold", color: green[900] }
                : { color: green[800] }
            }
          >
            {value}
          </Typography>
        </StyledTableCell>
      );
    case "NOLIFT":
      return (
        <StyledTableCell
          key={idx}
          align={column.align}
          sx={{ backgroundColor: red[100], borderColor: red[800] }}
        >
          <Typography sx={{ textDecoration: "line-through", color: red[900] }}>
            {value}
          </Typography>
        </StyledTableCell>
      );
    case "DNA":
      return (
        <StyledTableCell
          key={idx}
          align={column.align}
          sx={{
            backgroundColor: red[100],
            borderColor: red[800],
          }}
        >
          <Typography>{value}</Typography>
        </StyledTableCell>
      );
    default:
      console.log(column.extra);
      return (
        /* TODO: the styling is not working */
        <StyledTableCell key={idx} align={column.align} sx={column.extra}>
          <Typography>{value}</Typography>
        </StyledTableCell>
      );
  }
};

/* TODO: figure out how to make props into a list of predetermined strings
 * instead of using Record<string, any>  */
interface TableRowLinkProps extends Record<string, any> {}

const TableRowLink: React.FC<TableRowLinkProps> = (
  props: TableRowLinkProps
) => {
  const theme = useTheme();
  const { row, columns } = props;
  const { competition } = row;

  const renderLink = useMemo(
    () =>
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(function Link(
        itemProps,
        ref
      ) {
        return (
          <RouterLink
            to={`/competitions/${competition}`}
            ref={ref}
            {...itemProps}
            role={undefined}
            style={{ textDecoration: "none" }}
          />
        );
      }),
    [competition]
  );

  return (
    <TableRow
      sx={{
        "&:nth-of-type(odd)": {
          backgroundColor: grey[200],
        },
        "&:last-child td, &:last-child th": {
          border: 0,
        },
        "&:hover td": {
          backgroundColor: theme.palette.secondary.light,
        },
      }}
      component={renderLink}
    >
      {columns.map((column: any, idx: number) => isBestLift(idx, column, row))}
    </TableRow>
  );
};

interface RowProps extends Record<string, any> {}

interface CustomTableProps {
  rows: RowProps[]; // TODO: need to sort this type
  columns: any; // TODO: need to sort this type
}

const CustomTable: React.FC<CustomTableProps> = (props: CustomTableProps) => {
  const { rows, columns } = props;

  /* TODO groupByYear */
  /* const yearsGroupBy: string[] = []; */
  /**/
  /* function getYear(year: string) { */
  /*   if (yeary.includes(weightClass)) { */
  /*     return false; */
  /*   } else { */
  /*     yearsGroupBy.push(weightClass); */
  /*     return true; */
  /*   } */
  /* } */

  return (
    <TableContainer component={Paper}>
      <Table stickyHeader sx={{ minWidth: 650 }} aria-label="Competition Table">
        <TableHead>
          <TableRow>
            <StyledTableCell colSpan={5}></StyledTableCell>
            <StyledTableCell colSpan={3} align="center">
              Snatches
            </StyledTableCell>
            <StyledTableCell colSpan={3} align="center">
              Clean and Jerks
            </StyledTableCell>
            <StyledTableCell colSpan={2}></StyledTableCell>
          </TableRow>
          <TableRow>
            {columns.map((column: Column) => (
              <StyledTableCell key={column.id} align={column.align}>
                {column.label}
              </StyledTableCell>
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {/* TODO: fix row type */}
          {rows.map((row: RowProps, idx: number) => (
            <>
              {/* TODO groupbyYEAR */}
              {/* {getWeightClasses(row.weight_category) ? ( */}
              {/*   <TableRow> */}
              {/*     <StyledTableCell colSpan={13}> */}
              {/*       <Typography variant="h6"> */}
              {/*         {printWeightClasses(row.weight_category)} */}
              {/*       </Typography> */}
              {/*     </StyledTableCell> */}
              {/*   </TableRow> */}
              {/* ) : ( */}
              {/*   "" */}
              {/* )} */}
              <TableRowLink key={idx} row={row} columns={columns} />
            </>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CustomTable;
