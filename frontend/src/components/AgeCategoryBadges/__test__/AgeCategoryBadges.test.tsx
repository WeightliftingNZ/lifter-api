/** @format */

import React from "react";
import { describe, test, expect } from "@jest/globals";
import renderer from "react-test-renderer";
import AgeCategoryBadges from "../AgeCategoryBadges";

describe("Title component tests", () => {
  test.each(require("./ageCategoryData.json"))("renders", (testCase) => {
    const tree = renderer
      .create(<AgeCategoryBadges ageCategories={testCase} />)
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
