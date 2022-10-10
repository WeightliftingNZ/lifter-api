/** @format */

import React from "react";
import { describe, test, expect } from "@jest/globals";
import renderer from "react-test-renderer";
import Loading from "../Loading";

describe("Loading components tests", () => {
  test("renders", () => {
    const tree = renderer.create(<Loading />).toJSON();
    expect(tree).toMatchSnapshot();
  });
});
