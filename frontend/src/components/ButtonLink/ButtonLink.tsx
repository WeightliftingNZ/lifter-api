/** @format */

import { Button } from "@mui/material";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";
import React, { forwardRef, useMemo } from "react";
import { ButtonLinkProps } from "./interfaces";

const ButtonLink: React.FC<React.PropsWithChildren<ButtonLinkProps>> = (
  props
) => {
  const { to, size, color } = props;
  const renderLink = useMemo(
    () =>
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(function Link(
        itemProps,
        ref
      ) {
        return (
          <RouterLink
            to={to}
            ref={ref}
            {...itemProps}
            role={undefined}
            style={{ textDecoration: "none" }}
          />
        );
      }),
    [to]
  );
  return (
    <Button component={renderLink} size={size} color={color}>
      {props.children}
    </Button>
  );
};

export default ButtonLink;
