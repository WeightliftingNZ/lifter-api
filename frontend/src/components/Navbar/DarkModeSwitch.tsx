/** @format */

import React, { useContext } from "react";
import Switch from "@mui/material/Switch";
import LightModeOutlinedIcon from "@mui/icons-material/LightModeOutlined";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import { ColorModeContext } from "../../App";
import { useTheme } from "@mui/material/styles";

const DarkModeSwitch: React.FC = () => {
  const theme = useTheme();
  const colorMode = useContext(ColorModeContext);

  return (
    <Switch
      edge="start"
      color="secondary"
      checked={theme.palette.mode === "dark"}
      onChange={colorMode.toggleColorMode}
      inputProps={{ "aria-label": "dark-mode" }}
      icon={<LightModeOutlinedIcon />}
      checkedIcon={<DarkModeIcon />}
    />
  );
};

export default DarkModeSwitch;
