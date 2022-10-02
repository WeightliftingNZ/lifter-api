/** @format */

import React, { useMemo, forwardRef } from "react";
import {
  LinkProps as RouterLinkProps,
  Link as RouterLink,
} from "react-router-dom";
import {
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemProps,
  ListItemText,
} from "@mui/material";
import { useTheme } from "@mui/material/styles";

interface ListItemLinkProps extends ListItemProps {
  primary: React.ReactElement;
  to: string;
  icon?: React.ReactElement;
  open?: boolean;
}

const ListItemLink: React.FC<ListItemLinkProps> = ({
  primary,
  to,
  icon,
  open,
}) => {
  const theme = useTheme();
  const renderLink = useMemo(
    () =>
      forwardRef<HTMLAnchorElement, Omit<RouterLinkProps, "to">>(function Link(
        itemProps,
        ref
      ) {
        return <RouterLink to={to} ref={ref} {...itemProps} role={undefined} />;
      }),
    [to]
  );

  return (
    <ListItem component={renderLink}>
      <ListItemButton
        sx={{
          minHeight: 48,
          justifyContent: open ? "initial" : "center",
          px: 2.5,
        }}
      >
        {icon ? (
          <ListItemIcon
            sx={{
              minWidth: 0,
              mr: open ? 3 : "auto",
              justifyContent: "center",
            }}
          >
            {icon}
          </ListItemIcon>
        ) : null}
        <ListItemText
          sx={{
            textDecoration: "none",
            color:
              theme.palette.mode === "dark"
                ? theme.palette.primary.contrastText
                : theme.palette.primary.main,
            opacity: open ? 1 : 0,
          }}
          primary={primary}
        />
      </ListItemButton>
    </ListItem>
  );
};

export default ListItemLink;
