import React from "react";
import {
  Date,
  BidResponse,
  SlotResponse,
  TaskResponse,
  BidderResponse
} from "../../ResponseType";
import { List, ListSubheader } from "@mui/material";
import { ResponseCard } from "../field/ResponseCard";
type ResponseColumnProps = {
  day: Date | null;
  data: BidResponse[] | SlotResponse[] | TaskResponse[] |BidderResponse[];
};

export const ResponseColumn: React.FC<ResponseColumnProps> = (
  props: ResponseColumnProps
) => {
  return (
    <List
      sx={{
        width: "100%",
        maxWidth: 360,
        bgcolor: "background.paper",
        position: "relative",
        overflow: "auto",
        maxHeight: 680,
        "& ul": { padding: 0 },
      }}
      subheader={<li />}
    >
      {props.day ? (
        <ListSubheader>
          {props.day.month}月{props.day.day}日　{props.data.length}枠
        </ListSubheader>
      ) : (
        <ListSubheader>{props.data.length}個</ListSubheader>
      )}

      {props.data.map((bid) => (
        <ResponseCard data={bid} />
      ))}
    </List>
  );
};
