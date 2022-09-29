/** @format */

import { test } from "@jest/globals";
import { dateRangeProvider, printWeightCategories } from "../customFunctions";

test("dateRangeProvider", () => {
  expect(dateRangeProvider("2021-12-31", "2022-01-01")).toBe(
    "Fri, 31st Dec 2021 - Sat, 1st Jan 2022"
  );
  expect(dateRangeProvider("2022-01-31", "2022-02-01")).toBe(
    "Mon, 31st Jan - Tue, 1st Feb 2022"
  );
  expect(dateRangeProvider("2022-01-02", "2022-01-03")).toBe(
    "Sun, 2nd - Mon, 3rd Jan 2022"
  );
  expect(dateRangeProvider("2022-01-02", "2022-01-02")).toBe(
    "Sun, 2nd Jan 2022"
  );
});

test("printWeightCategories", () => {
  expect(printWeightCategories("W90+")).toBe("Women's 90+ kg");
  expect(printWeightCategories("M96")).toBe("Men's 96 kg");
});
