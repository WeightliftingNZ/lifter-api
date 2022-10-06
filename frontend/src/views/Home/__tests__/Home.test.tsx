/** @format */

import React from "react";
import { test, expect } from "@jest/globals";
import renderer from "react-test-renderer";
import Home from "../Home";

test.skip("render correctly", () => {
  const tree = renderer.create(<Home />).toJSON();

  expect(tree).toMatchSnapshot();
});
