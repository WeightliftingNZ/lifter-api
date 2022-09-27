/** @format */

import { test } from "@jest/globals";
import { titleMaker } from "../customFunctions";

test("titleMaker", () => {
  expect(titleMaker("make_title")).toBe("Make Title");
});
