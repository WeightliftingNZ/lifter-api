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

interface Column {
  id: keyof LiftObjectProps;
  label: string;
  minWidth?: number;
  align?: "right" | "left" | "center";
  format?: (value: number) => string;
  sx?: any;
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
  { id: "total_lifted", label: "Total", sx: { fontWeight: "bold" } },
  { id: "placing", label: "Place" },
];

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
          />
        );
      }),
    [athlete]
  );

  const determineLift = (liftStatus: string) => {
    if (liftStatus === "NOLIFT") {
      return { backgroundColor: "red" };
    } else if (liftStatus === "LIFT") {
      return { backgroundColor: "green" };
    } else if (liftStatus === "NOLIFT") {
      return { backgroundColor: "grey" };
    }
  };

  const giveLift = (liftId: keyof LiftObjectProps, currentRow: any) => {
    let isBold = false; // if the lift is the best lift
    let strikeThrough = false; // if no lift, strike through

    const bestSnatch = currentRow.best_snatch_weight[0];
    const bestCnj = currentRow.best_cnj_weight[0];

    switch (liftId.replace("_weight", "")) {
      case "snatch_first":
        if (bestSnatch === "1st") {
          isBold = true;
        }
        break;
      case "snatch_second":
        if (bestSnatch === "2nd") {
          isBold = true;
        }
        break;
      case "snatch_third":
        if (bestSnatch === "3rd") {
          isBold = true;
        }
        break;
      case "cnj_first":
        if (bestCnj === "1st") {
          isBold = true;
        }
        break;
      case "cnj_second":
        if (bestCnj === "2nd") {
          isBold = true;
        }
        break;
      case "cnj_third":
        if (bestCnj === "3rd") {
          isBold = true;
        }
        break;
    }

    return (
      <>{isBold ? <b>{currentRow[liftId]}</b> : <>{currentRow[liftId]}</>}</>
    );
  };

  return (
    <TableRow
      sx={{
        "&:nth-of-type(odd)": {
          backgroundColor: theme.palette.action.hover,
        },
        "&:last-child td, &:last-child th": {
          border: 0,
        },
      }}
      component={renderLink}
    >
      {columns.map((column: any, idx: number) => (
        <StyledTableCell key={idx} align={column.align}>
          <Typography variant="body1">{giveLift(column.id, row)}</Typography>
        </StyledTableCell>
      ))}
    </TableRow>
  );
};

interface RowProps extends Record<string, any> {}

interface CustomTableProps {
  rows: RowProps[]; // TODO: need to sort this type
  columns: any; // TODO: need to sort this type
}

const CustomTable: React.FC<CustomTableProps> = (props: CustomTableProps) => {
  const { rows } = props;

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
            <TableRowLink key={idx} row={row} columns={columns} />
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CustomTable;
