/** @format */

import React from "react";
import { describe, test, expect } from "@jest/globals";
import renderer from "react-test-renderer";
import Title from "../Title";

describe("Title component tests", () => {
  test("renders without text", () => {
    const tree = renderer.create(<Title></Title>).toJSON();
    expect(tree).toMatchSnapshot();
  });
  test("renders with text", () => {
    const tree = renderer.create(<Title>Test Text</Title>).toJSON();
    expect(tree).toMatchSnapshot();
  });
  test("renders with text and props", () => {
    const tree = renderer
      .create(<Title sx={{ textAlign: "left" }}>Test Text</Title>)
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
