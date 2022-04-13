import React, { useMemo } from "react";
import { useTable } from "react-table";
import { liftColumns } from "./liftColumns";

const LiftsTable = ({ lifts }: any) => {
  const liftData = useMemo(() => [...lifts], [lifts]);
  const liftColumnsMemo = useMemo(() => liftColumns, []);
  const weightClasses = [""];

  function groupByWeightClasses(weightClass: string) {
    if (weightClasses.includes(weightClass)) {
      return false;
    }
    weightClasses.push(weightClass);
    return true;
  }

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable({ columns: liftColumnsMemo, data: liftData } as any);

  if (lifts.length === 0) {
    return (
      <>
        <div>This session has no lifts.</div>
      </>
    );
  }

  return (
    <>
      <table {...getTableProps}>
        <thead>
          {headerGroups.map((headerGroup, idx) => (
            <tr {...headerGroup.getHeaderGroupProps()} key={idx}>
              {headerGroup.headers.map((column, idx) => (
                <th {...column.getHeaderProps()} key={idx}>
                  {column.render("Header")}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody {...getTableBodyProps()}>
          {rows.map((row, idx) => {
            prepareRow(row);
            return (
              <React.Fragment key={idx}>
                {groupByWeightClasses(row.cells[3].value) ? (
                  <tr>
                    <td>{row.cells[3].value}</td>
                  </tr>
                ) : null}
                <tr
                  {...row.getRowProps()}
                  className={
                    idx % 2 !== 0
                      ? "bg-slate-300 hover:bg-slate-400"
                      : "bg-slate-100 hover:bg-slate-200"
                  }
                  key={idx}
                >
                  {row.cells.map((cell, idx) => {
                    return (
                      <td {...cell.getCellProps()} key={idx}>
                        {cell.render("Cell")}
                      </td>
                    );
                  })}
                </tr>
              </React.Fragment>
            );
          })}
        </tbody>
      </table>
    </>
  );
};

export default LiftsTable;
