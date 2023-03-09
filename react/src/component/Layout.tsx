import React from "react";
import { Outlet } from "react-router-dom";
import PositionedMenu from "./PositionedMenu";
import { Stack } from "@mui/system";
import AccountMenu from "./AcountMenu";
import { UserContext } from "../UserContext";
export const Layout: React.FC = () => {
  const {user}=React.useContext(UserContext)
  return (
    <div>
      <ul>
        <Stack direction={"row"}>
          <PositionedMenu />
          <AccountMenu />
          <p>{user.point}</p>
          <p>{user.name}</p>
        </Stack>
      </ul>
      <Outlet />
      <ul>
        <h4>Footer</h4>
      </ul>
    </div>
  );
};
