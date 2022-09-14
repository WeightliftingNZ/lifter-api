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
import { LiftObjectProps } from "../../interfaces";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";
import { useTheme } from "@mui/material/styles";
import Typography from "@mui/material/Typography";
import { red, green } from "@mui/material/colors";

interface Column {
  id: keyof LiftObjectProps;
  label: string;
  minWidth?: number;
  align?: "right" | "left" | "center";
  format?: (value: number) => string;
}

const columns: Column[] = [
  { id: "lottery_number", label: "Lott." },
  { id: "athlete_name", label: "Name" },
  { id: "athlete_yearborn", label: "Birthyear" },
  { id: "team", label: "Team" },
  { id: "bodyweight", label: "Weight" },
  { id: "snatch_first_weight", label: "1", align: "center" },
  { id: "snatch_second_weight", label: "2", align: "center" },
  { id: "snatch_third_weight", label: "3", align: "center" },
  { id: "cnj_second_weight", label: "1", align: "center" },
  { id: "cnj_first_weight", label: "2", align: "center" },
  { id: "cnj_third_weight", label: "3", align: "center" },
  { id: "total_lifted", label: "Total", align: "center" },
  { id: "placing", label: "Place", align: "center" },
];

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
      return (
        <StyledTableCell key={idx} align={column.align}>
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
  const { row } = props;
  const { athlete } = row;

  const renderLink = useMemo(
    () =>
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(function Link(
        itemProps,
        ref
      ) {
        return (
          <RouterLink
            to={`/athletes/${athlete}`}
            ref={ref}
            {...itemProps}
            role={undefined}
            style={{ textDecoration: "none" }}
          />
        );
      }),
    [athlete]
  );

  return (
    <TableRow
      sx={{
        "&:nth-of-type(odd)": {
          backgroundColor: theme.palette.primary.light,
        },
        "&:last-child td, &:last-child th": {
          border: 0,
        },
        "&:hover td": {
          backgroundColor: theme.palette.primary.dark,
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
  const theme = useTheme();
  const { rows } = props;

  const weightClasses: string[] = [];

  function getWeightClasses(weightClass: string) {
    if (weightClasses.includes(weightClass)) {
      return false;
    } else {
      weightClasses.push(weightClass);
      return true;
    }
  }

  function printWeightClasses(weightClass: string) {
    return `${weightClass.replace("W", "Women's ").replace("M", "Men's ")} kg`;
  }

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
              {getWeightClasses(row.weight_category) ? (
                <TableRow>
                  <StyledTableCell colSpan={13}>
                    <Typography variant="h6">
                      {printWeightClasses(row.weight_category)}
                    </Typography>
                  </StyledTableCell>
                </TableRow>
              ) : (
                ""
              )}
              <TableRowLink key={idx} row={row} columns={columns} />
            </>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CustomTable;
