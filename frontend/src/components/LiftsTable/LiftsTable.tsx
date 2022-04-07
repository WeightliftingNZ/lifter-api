import React, { useMemo } from "react";
import { useGroupBy, useExpanded, useTable } from "react-table";
import { liftColumns } from "./liftColumns";

const LiftsTable = ({ lifts }: any) => {
  const liftData = useMemo(() => [...lifts], [lifts]);
  const liftColumnsMemo = useMemo(() => liftColumns, []);

  const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
    useTable(
      { columns: liftColumnsMemo, data: liftData } as any,
      useGroupBy,
      useExpanded
    );

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
            );
          })}
        </tbody>
      </table>
    </>
  );
};

export default LiftsTable;
