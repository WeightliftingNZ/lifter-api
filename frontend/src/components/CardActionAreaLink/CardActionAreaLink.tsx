import React, { forwardRef, useMemo } from "react";
import { CardActionArea } from "@mui/material";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";

interface CardActionAreaProps {
  to: string;
  children?: React.ReactNode;
}

const CardActionAreaLink: React.FC<
  React.PropsWithChildren<CardActionAreaProps>
> = (props: CardActionAreaProps) => {
  const { to } = props;
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
    <CardActionArea component={renderLink}>{props.children}</CardActionArea>
  );
};

export default CardActionAreaLink;
