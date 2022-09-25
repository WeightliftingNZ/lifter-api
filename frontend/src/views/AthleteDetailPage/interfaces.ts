/** @format */

import { LiftObjectProps } from "../../interfaces";

export interface Column {
  id: keyof LiftObjectProps;
  label: string;
  minWidth?: number;
  align?: "right" | "left" | "center";
  format?: (value: number) => string;
  extra?: { [key: string]: string };
}
