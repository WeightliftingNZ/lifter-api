/** @format */

import React from "react";
import { describe, test, expect } from "@jest/globals";
import renderer from "react-test-renderer";
import Error from "../Error";

describe("Error components tests", () => {
  test("renders", () => {
    const tree = renderer.create(<Error />).toJSON();
    expect(tree).toMatchSnapshot();
  });
});
