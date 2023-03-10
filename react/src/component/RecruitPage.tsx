import * as React from "react";
import Tabs from "@mui/material/Tabs";
import Tab from "@mui/material/Tab";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { BidList } from "./list/BidList";
import { SlotList } from "./list/SlotList";
import { useNavigate } from "react-router-dom";
import { CreateCard } from "./field/NewCreateCard";
interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          <Typography>{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    "aria-controls": `simple-tabpanel-${index}`,
  };
}

export const TabContext = React.createContext(0);

export const BidPage: React.FC = () => {
  const [value, setValue] = React.useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const navigate = useNavigate();

  return (
    <TabContext.Provider value={value }>
    <Box sx={{ width: "100%" }}>
      <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
        <Tabs
          value={value}
          onChange={handleChange}
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab label="参加予定の仕事" {...a11yProps(0)} />
            <Tab label="募集中" {...a11yProps(1)} />
            <Tab label='交代申請中' {...a11yProps(2)} />
          <Tab label="人数不足中" {...a11yProps(3)} />
          <Tab label="経験が不足中" {...a11yProps(4)} />
          <Tab label="完了したシフト" {...a11yProps(5)} />
          <Tab label="募集した仕事" {...a11yProps(6)} />
          <Tab label="作成したタスク" {...a11yProps(7)} />
        </Tabs>
      </Box>
      <TabPanel value={value} index={0}>
        <SlotList url="/assigned" />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <BidList url="/bids/open" />
        </TabPanel>
        <TabPanel value={value} index={2}>
        <BidList url="/bids/open" />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <BidList url="/bids/lack" />
      </TabPanel>
      <TabPanel value={value} index={4}>
        <BidList url="/bids/lack_exp" />
      </TabPanel>
      <TabPanel value={value} index={5}>
        終わったシフト
      </TabPanel>
      <TabPanel value={value} index={6}>
        <CreateCard
          text="新しく仕事を募集"
          onClick={() => {
            navigate("/newslot");
          }}
        />
        <SlotList url="/createslot" />
      </TabPanel>
      <TabPanel value={value} index={7}>
        <CreateCard
          text="新しいタスクを作成"
          onClick={() => {
            navigate("/newtask");
          }}
        />
        <SlotList url="/createtask" />
      </TabPanel>
      </Box>
      </TabContext.Provider>
  );
};
