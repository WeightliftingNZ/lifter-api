/** @format */

import React, { useState, forwardRef, useMemo, PropsWithChildren } from "react";
import {
  Link as RouterLink,
  LinkProps as RouterLinkProps,
} from "react-router-dom";
import Divider from "@mui/material/Divider";
import MuiAppBar, { AppBarProps as MuiAppBarProps } from "@mui/material/AppBar";
import CssBaseline from "@mui/material/CssBaseline";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import PeopleIcon from "@mui/icons-material/People";
import EmojiEventsIcon from "@mui/icons-material/EmojiEvents";
import ChevronLeftIcon from "@mui/icons-material/ChevronLeft";
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import { styled, useTheme } from "@mui/material/styles";
import Button from "@mui/material/Button";
import NavbarSearch from "./NavbarSearch";
import { Box, Container, Drawer } from "@mui/material";
import { Stack } from "@mui/system";
import DarkModeSwitch from "./DarkModeSwitch";
import SearchIcon from "@mui/icons-material/Search";

const drawerWidth = 240;

const Main = styled("main", { shouldForwardProp: (prop) => prop !== "open" })<{
  open?: boolean;
}>(({ theme, open }) => ({
  flexGrow: 1,
  paddingTop: theme.spacing(3),
  transition: theme.transitions.create("margin", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  marginLeft: `-${drawerWidth}px`,
  ...(open && {
    transition: theme.transitions.create("margin", {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginLeft: 0,
  }),
}));

interface ListItemLinkProps {
  primary: string;
  to: string;
  icon?: React.ReactElement;
  open?: boolean;
}

const links: ListItemLinkProps[] = [
  { primary: "Competition", to: "/competitions", icon: <EmojiEventsIcon /> },
  { primary: "Athlete", to: "/athletes", icon: <PeopleIcon /> },
];

const ListItemLink: React.FC<ListItemLinkProps> = ({
  icon,
  primary,
  to,
  open,
}) => {
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
    <List>
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
          <ListItemText sx={{ opacity: open ? 1 : 0 }} primary={primary} />
        </ListItemButton>
      </ListItem>
    </List>
  );
};

const NavbarHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
}));

const DrawerHeader = styled("div")(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "flex-end",
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
}));

interface AppBarProps extends MuiAppBarProps {
  open?: boolean;
}

const AppBar = styled(MuiAppBar, {
  shouldForwardProp: (prop) => prop !== "open",
})<AppBarProps>(({ theme, open }) => ({
  transition: theme.transitions.create(["width", "margin"], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(["width", "margin"], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

interface HeaderBarProps {
  open: boolean;
  handleDrawerOpen: any;
}

const HeaderBar: React.FC<HeaderBarProps> = ({ open, handleDrawerOpen }) => {
  const theme = useTheme();
  const [showSearchOnly, setShowSearchOnly] = useState<boolean>(false);

  const handleSearchOnClick = () => {
    setShowSearchOnly(true);
  };

  const handleSearchOnBlur = () => {
    setShowSearchOnly(false);
  };

  return (
    <AppBar position="fixed" open={open}>
      <Toolbar
        sx={{
          display: "flex",
          flexWrap: "nowrap",
          flexDirection: "row",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        {showSearchOnly ? (
          <Box
            sx={{
              flexGrow: 1,
              px: 2,
            }}
          >
            <NavbarSearch handleSearchOnBlur={handleSearchOnBlur} />
          </Box>
        ) : (
          <>
            <Box
              sx={{
                display: "flex",
                alignItems: "center",
                flexWrap: "nowrap",
                gap: 1,
              }}
            >
              <IconButton
                color="inherit"
                aria-label="open drawer"
                onClick={handleDrawerOpen}
                edge="start"
                sx={{
                  marginRight: 0,
                  ...(open && { display: { sm: "none" } }),
                }}
              >
                <MenuIcon />
              </IconButton>
              <Button component={RouterLink} to="/">
                <Stack>
                  <Typography
                    noWrap
                    component="div"
                    sx={{ color: theme.palette.primary.contrastText }}
                  >
                    Weightlifting
                  </Typography>
                  <Typography
                    noWrap
                    component="div"
                    sx={{ color: theme.palette.primary.contrastText }}
                  >
                    New Zealand
                  </Typography>
                </Stack>
              </Button>
              <IconButton onClick={handleSearchOnClick}>
                <SearchIcon htmlColor={theme.palette.secondary.main} />
              </IconButton>
            </Box>
            <Box>
              <DarkModeSwitch />
            </Box>
          </>
        )}
      </Toolbar>
    </AppBar>
  );
};

const Navbar: React.FC<PropsWithChildren> = (props) => {
  const theme = useTheme();
  const [open, setOpen] = useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };
  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <HeaderBar handleDrawerOpen={handleDrawerOpen} open={open} />
      <Drawer
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
        variant="persistent"
        open={open}
      >
        <DrawerHeader>
          <IconButton onClick={handleDrawerClose}>
            {theme.direction === "rtl" ? (
              <ChevronRightIcon />
            ) : (
              <ChevronLeftIcon />
            )}
          </IconButton>
        </DrawerHeader>
        <Divider />
        {links.map((link, idx) => {
          return (
            <ListItemLink
              key={idx}
              icon={link.icon}
              to={link.to}
              primary={link.primary}
              open={open}
            />
          );
        })}
      </Drawer>
      <Main open={open}>
        <NavbarHeader />
        <Container disableGutters maxWidth="lg">
          {props.children}
        </Container>
      </Main>
    </Box>
  );
};

export default Navbar;
