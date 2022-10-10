/** @format */

import React from "react";
import { describe, test, expect } from "@jest/globals";
import renderer from "react-test-renderer";
import Body from "../Body";

describe("Title component tests", () => {
  test("renders without text", () => {
    const tree = renderer.create(<Body></Body>).toJSON();
    expect(tree).toMatchSnapshot();
  });
  test("renders with text", () => {
    const tree = renderer.create(<Body>Test Text</Body>).toJSON();
    expect(tree).toMatchSnapshot();
  });
  test("renders with text and props", () => {
    const tree = renderer
      .create(<Body sx={{ textAlign: "left" }}>Test Text</Body>)
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
