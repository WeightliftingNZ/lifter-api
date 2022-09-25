/** @format */

import React from "react";

const LiftTable = () => {
  return <></>;
};

export default LiftTable;

/* const parseLiftCells = ( */
/*   idx: number, */
/*   column: Column, */
/*   currentRow: LiftObjectProps */
/* ) => { */
/*   let isBold = false; // if the lift is the best lift */
/*   let currentLiftStatus = ""; */
/*   let value = currentRow[column.id]; */
/**/
/*   const bestSnatch = currentRow.best_snatch_weight[0]; */
/*   const bestCnj = currentRow.best_cnj_weight[0]; */
/**/
/*   switch (column.id.replace("_weight", "")) { */
/*     case "snatch_first": */
/*       if (bestSnatch === "1st") { */
/*         isBold = true; */
/*       } */
/*       currentLiftStatus = currentRow.snatches["1st"].lift_status; */
/*       if (currentLiftStatus === "DNA") { */
/*         value = "-"; */
/*       } */
/*       break; */
/*     case "snatch_second": */
/*       if (bestSnatch === "2nd") { */
/*         isBold = true; */
/*       } */
/*       currentLiftStatus = currentRow.snatches["2nd"].lift_status; */
/*       if (currentLiftStatus === "DNA") { */
/*         value = "-"; */
/*       } */
/*       break; */
/*     case "snatch_third": */
/*       if (bestSnatch === "3rd") { */
/*         isBold = true; */
/*       } */
/*       currentLiftStatus = currentRow.snatches["3rd"].lift_status; */
/*       if (currentLiftStatus === "DNA") { */
/*         value = "-"; */
/*       } */
/*       break; */
/*     case "cnj_first": */
/*       if (bestCnj === "1st") { */
/*         isBold = true; */
/*       } */
/*       currentLiftStatus = currentRow.cnjs["1st"].lift_status; */
/*       if (currentLiftStatus === "DNA") { */
/*         value = "-"; */
/*       } */
/*       break; */
/*     case "cnj_second": */
/*       if (bestCnj === "2nd") { */
/*         isBold = true; */
/*       } */
/*       currentLiftStatus = currentRow.cnjs["2nd"].lift_status; */
/*       if (currentLiftStatus === "DNA") { */
/*         value = "-"; */
/*       } */
/*       break; */
/*     case "cnj_third": */
/*       if (bestCnj === "3rd") { */
/*         isBold = true; */
/*       } */
/*       currentLiftStatus = currentRow.cnjs["3rd"].lift_status; */
/*       if (currentLiftStatus === "DNA") { */
/*         value = "-"; */
/*         break; */
/*       } */
/*   } */
/**/
/*   switch (currentLiftStatus) { */
/*     case "LIFT": */
/*       return ( */
/*         <StyledTableCell */
/*           key={idx} */
/*           align={column.align} */
/*           sx={ */
/*             isBold */
/*               ? { */
/*                   backgroundColor: green[100], */
/*                   borderWidth: 3, */
/*                   borderColor: green[800], */
/*                 } */
/*               : { backgroundColor: green[100], borderColor: green[800] } */
/*           } */
/*         > */
/*           <Typography */
/*             sx={ */
/*               isBold */
/*                 ? { fontWeight: "bold", color: green[900] } */
/*                 : { color: green[800] } */
/*             } */
/*           > */
/*             {value} */
/*           </Typography> */
/*         </StyledTableCell> */
/*       ); */
/*     case "NOLIFT": */
/*       return ( */
/*         <StyledTableCell */
/*           key={idx} */
/*           align={column.align} */
/*           sx={{ backgroundColor: red[100], borderColor: red[800] }} */
/*         > */
/*           <Typography sx={{ textDecoration: "line-through", color: red[900] }}> */
/*             {value} */
/*           </Typography> */
/*         </StyledTableCell> */
/*       ); */
/*     case "DNA": */
/*       return ( */
/*         <StyledTableCell */
/*           key={idx} */
/*           align={column.align} */
/*           sx={{ */
/*             backgroundColor: red[100], */
/*             borderColor: red[800], */
/*           }} */
/*         > */
/*           <Typography>{value}</Typography> */
/*         </StyledTableCell> */
/*       ); */
/*     default: */
/*       return ( */
/*         /* TODO: the styling is not working */
/*         <StyledTableCell key={idx} align={column.align} sx={column.extra}> */
/*           <Typography>{value}</Typography> */
/*         </StyledTableCell> */
/*       ); */
/*   } */
/* }; */
