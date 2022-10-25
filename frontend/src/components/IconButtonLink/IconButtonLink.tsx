/** @format */

import React, { forwardRef, useMemo } from "react";
import { IconButton } from "@mui/material";
import { IconButtonLinkProps } from "./interfaces";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";

const IconButtonLink: React.FC<React.PropsWithChildren<IconButtonLinkProps>> = (
  props
) => {
  const { to } = props;
  const renderLink = useMemo(
    () =>
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(
        function Link(itemProps, ref) {
          return (
            <RouterLink
              to={to}
              ref={ref}
              {...itemProps}
              role={undefined}
              style={{ textDecoration: "none" }}
            />
          );
        }
      ),
    [to]
  );
  return <IconButton component={renderLink}>{props.children}</IconButton>;
};

export default IconButtonLink;
