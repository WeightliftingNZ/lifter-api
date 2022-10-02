/** @format */

import React from "react";
import SubTitle from "../SubTitle";
import { LastUpdatedProps } from "./interfaces";
import moment from "moment";

const LastUpdated: React.FC<LastUpdatedProps> = (props) => {
  const dates = props.update
    .map((date) => moment(date))
    .sort((a: any, b: any) => a - b);
  return <SubTitle>Last updated {dates[0].fromNow()}</SubTitle>;
};

export default LastUpdated;
