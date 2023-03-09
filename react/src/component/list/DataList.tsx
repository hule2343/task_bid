import * as React from "react";
import axios from "../../axios";
import useSWR, { Fetcher } from "swr";
import { ScrollMenu } from "react-horizontal-scrolling-menu";
import { ResponseColumn } from "./ResponseColumn";
import {
  Date,
  BidResponse,
  SlotResponse,
  ListProps,

} from "../../ResponseType";
import { isSlot, isBid } from "../field/ResponseCard";

export const uniquedays = (days: any[]) =>
  days.filter((value, index) => {
    const _value = JSON.stringify(value);
    return (
      index ===
      days.findIndex((day) => {
        return JSON.stringify(day) === _value;
      })
    );
  });

export const daysort = (days: Date[]): Date[] => {
  return days.sort((a: Date, b: Date) => {
    if (a.year === b.year) {
      if (a.month === b.month) {
        return a.day < b.day ? -1 : 1;
      } else return a.month < b.month ? -1 : 1;
    } else return a.year < b.year ? -1 : 1;
  });
};

const getDatas: Fetcher<any[]> = (url: string) => {
  return axios.get(url).then((response) => response.data);
};

export const DataList: React.FC<ListProps> = (props: ListProps) => {
  const { data, error } = useSWR(props.url, getDatas);
  if (error) return <div>Loading Failed</div>;
  if (!data) return <div>loading...</div>;
  const days: Date[] | null = isSlot(data[0])
    ? daysort(
        uniquedays(
          Array.from(
            data.map((slot: SlotResponse): Date => {
              return {
                year: slot.start_time.year,
                month: slot.start_time.month,
                day: slot.start_time.day,
              };
            })
          )
        )
      )
    : isBid(data[0])
    ? daysort(
        uniquedays(
          Array.from(
            data.map((bid: BidResponse): Date => {
              return {
                year: bid.slot.start_time.year,
                month: bid.slot.start_time.month,
                day: bid.slot.start_time.day,
              };
            })
          )
        )
      )
    : null;

  return (
    <>
      <ScrollMenu>
        {days === null ? (
          <ResponseColumn day={null} data={data} />
        ) : isSlot(data[0]) ? (
          days.map((day: Date) => {
            return (
              <ResponseColumn
                day={day}
                data={data.filter((slot: SlotResponse) => {
                  return (
                    slot.start_time.year === day.year &&
                    slot.start_time.month === day.month &&
                    slot.start_time.day === day.day
                  );
                })}
              />
            );
          })
        ) : isBid(data[0]) ? (
          days.map((day: Date) => {
            return (
              <ResponseColumn
                day={day}
                data={data.filter((bid: BidResponse) => {
                  return (
                    bid.slot.start_time.year === day.year &&
                    bid.slot.start_time.month === day.month &&
                    bid.slot.start_time.day === day.day
                  );
                })}
              />
            );
          })
        ) : (
          <></>
        )}
      </ScrollMenu>
    </>
  );
};
