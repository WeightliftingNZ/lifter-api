/** @format */

import React from "react";
import { LiftObjectProps } from "../../interfaces";
import LiftCell from "./LiftCell";

interface LiftCellProps extends LiftObjectProps {
  to?: string | { pathname: string; hash: string };
}

const LiftCells: React.FC<LiftCellProps> = ({
  to,
  best_snatch_weight,
  best_cnj_weight,
  snatch_first,
  snatch_first_weight,
  snatch_second,
  snatch_second_weight,
  snatch_third,
  snatch_third_weight,
  cnj_first,
  cnj_first_weight,
  cnj_second,
  cnj_second_weight,
  cnj_third,
  cnj_third_weight,
}) => {
  const best_snatch = best_snatch_weight[0];
  const best_cnj = best_cnj_weight[0];

  return (
    <>
      <LiftCell
        isBest={best_snatch === "1st"}
        liftStatus={snatch_first}
        weight={snatch_first_weight}
        to={to}
      />
      <LiftCell
        isBest={best_snatch === "2nd"}
        liftStatus={snatch_second}
        weight={snatch_second_weight}
        to={to}
      />
      <LiftCell
        isEnd
        isBest={best_snatch === "3rd"}
        liftStatus={snatch_third}
        weight={snatch_third_weight}
        to={to}
      />
      <LiftCell
        isBest={best_cnj === "1st"}
        liftStatus={cnj_first}
        weight={cnj_first_weight}
        to={to}
      />
      <LiftCell
        isBest={best_cnj === "2nd"}
        liftStatus={cnj_second}
        weight={cnj_second_weight}
        to={to}
      />
      <LiftCell
        isBest={best_cnj === "3rd"}
        liftStatus={cnj_third}
        weight={cnj_third_weight}
        to={to}
      />
    </>
  );
};

export default LiftCells;
