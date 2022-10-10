/** @format */

import React from "react";
import { describe, test, expect } from "@jest/globals";
import renderer from "react-test-renderer";
import SubTitle from "../SubTitle";

describe("SubTitle components tests", () => {
  test("renders without text", () => {
    const tree = renderer.create(<SubTitle></SubTitle>).toJSON();
    expect(tree).toMatchSnapshot();
  });
  test("renders with text", () => {
    const tree = renderer.create(<SubTitle>Test Text</SubTitle>).toJSON();
    expect(tree).toMatchSnapshot();
  });
  test("renders with text and props", () => {
    const tree = renderer
      .create(
        <SubTitle sx={{ textDecoration: "underline" }}>Test Text</SubTitle>
      )
      .toJSON();
    expect(tree).toMatchSnapshot();
  });
});
