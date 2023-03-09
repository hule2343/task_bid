import * as React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import {
  ResponseBase,
  BidResponse,
  SlotResponse,
  TaskResponse,
  BidderResponse,
} from "../../ResponseType";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogTitle from "@mui/material/DialogTitle";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import { SingleChoiceField } from "./SIngleChoiceField";
import { DateSelect } from "./DateSelect";
import { Box } from "@mui/material";
import dayjs, { Dayjs } from "dayjs";
import { SimpleChoiceField } from "./SimpleChoiceField";
import { TabContext } from "../RecruitPage";
import axios from "../../axios";
import { useSnackbar } from "../Snackbar";
type ResponseCardProps<T extends ResponseBase> = {
  data: T;
};

type ResponseDisplayProps = {
  data: BidResponse | SlotResponse | TaskResponse | BidderResponse;
};

interface ModalData {
  id: string;
  name: string;
  start_point?: number;
  buyout_point?: number;
}

type ModalProps = {
  data: ResponseBase;
};

type BidderModalProps = {
  data: BidderResponse;
};

type ResponseModalProps = {
  open: boolean;
  handleClose: () => void;
  handleSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
  data: BidResponse | SlotResponse | TaskResponse|BidderResponse;
};

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export const ResponseCard: React.FC<
  ResponseCardProps<BidResponse | SlotResponse | TaskResponse|BidderResponse>
> = (props: ResponseCardProps<BidResponse | SlotResponse |TaskResponse|BidderResponse>) => {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  return (
    <Card
      style={{
        width: "240px",
        display: "inline-block",
      }}
    >
      <CardContent>
        <Typography gutterBottom variant="h6" component="div">
          {props.data.name}
        </Typography>
        <ResponseDisplay data={props.data} />
      </CardContent>
      <CardActions>
        <Button size="small">Share</Button>
        <Button size="small" onClick={handleOpen}>
          Open modal
        </Button>
        <ResponseModalBase
          open={open}
          handleClose={handleClose}
          handleSubmit={(event) => {}}
          data={props.data}
        />
      </CardActions>
    </Card>
  );
};

const ResponseModalBase: React.FC<ResponseModalProps> = (
  props: ResponseModalProps
) => {
  const value = React.useContext(TabContext);
  return (
    <Dialog open={props.open} onClose={props.handleClose}>
      <DialogTitle>Subscribe</DialogTitle>
      <DialogContent>
        <DialogContentText>
          To subscribe to this website, please enter your email address here. We
          will send updates occasionally.
        </DialogContentText>
        {value === 0 && isSlot(props.data)? (
          <AssignModalField data={props.data} />
        ) : value === 1 && isBid(props.data) ? (
          <TenderModalField data={props.data} />
        ) : value === 2 && isBidder(props.data) ? (
          <ConvertModalField data={props.data} />
        ) : value === 3 && isBid(props.data) ? (
          <LackModalField data={props.data} />
        ) : value === 4 && isBid(props.data) ? (
          <LackExpModalField data={props.data} />
        ) : value === 5 && isSlot(props.data) ? (
          <CheckWorkModalField data={props.data} />
        ) : value === 6 && isSlot(props.data) ? (
          <SlotModalField data={props.data} />
        ) : value === 7 && isTask(props.data) ? (
          <TaskModalField data={props.data} />
        ) : (
          <div>Failed to load data</div>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={props.handleClose}>Cancel</Button>
      </DialogActions>
    </Dialog>
  );
};

const AssignModalField: React.FC<ModalProps> = (props: ModalProps) => {
  const {showSnackbar}=useSnackbar()
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/slots/${props.data.id}/cancel`, {
        premire_point: data.get("premire_point"),
      })
      .then((response) => {
        showSnackbar('更新成功','success')
        console.log(response);
      })
      .catch((err) => {
        showSnackbar('更新失敗','error')
        console.log(err);
      });
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid item xs={12}>
        <TextField
          id="premire_point"
          name="premire_point"
          inputProps={{ min: "0", step: "1" }}
          label="加算ポイント"
          defaultValue="0"
          type="number"
        />
      </Grid>
      <Button type="submit">交代を申請する</Button>
    </Box>
  );
};

const TenderModalField: React.FC<ResponseCardProps<BidResponse>> = (
  props: ResponseCardProps<BidResponse>
) => {
  const {showSnackbar}=useSnackbar()
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    if(props.data.user_bidpoint === 'notyet') {
      axios
      .post(`/bids/${props.data.id}/tender`, {
        tender_point: data.get("tender_point"),
      })
      .then((response) => {
        showSnackbar('更新成功','success')
        console.log(response);
        console.log(props.data.user_bidpoint)
      })
        .catch((err) => {
          showSnackbar('更新失敗','error')
        console.log(err);
      });
    }else {
      axios.patch(`/bids/${props.data.id}`,{
        tender_point: data.get("tender_point"),
      }).then((response) => {
        console.log(response);
      })
      .catch((err) => {
        console.log(err);
      });
    }
    
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid item xs={12}>
        <TextField
          id="tender_point"
          name="tender_point"
          inputProps={{ min: String(props.data.buyout_point),max:String(props.data.start_point), step: "1" }}
          label="入札ポイント"
          defaultValue={String(props.data.start_point)}
          type="number"
        />
      </Grid>
      <Button type="submit">入札する</Button>
    </Box>
  );
};

const LackModalField: React.FC<ResponseCardProps<BidResponse>> = (
  props: ResponseCardProps<BidResponse>
) => {
  const {showSnackbar}=useSnackbar()
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/bids/${props.data.id}/tenderlack`)
      .then((response) => {
        showSnackbar('更新成功','success')
        console.log(response);
      })
      .catch((err) => {
        showSnackbar('更新失敗','error')
        console.log(err);
      });
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid item xs={12}></Grid>
      <Button type="submit">参加する</Button>
    </Box>
  );
};

const LackExpModalField: React.FC<ResponseCardProps<BidResponse>> = (
  props: ResponseCardProps<BidResponse>
) => {
  const {showSnackbar}=useSnackbar()
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/bids/${props.data.id}/tenderlack`)
      .then((response) => {
        showSnackbar('更新成功','success')
        console.log(response);
      })
      .catch((err) => {
        showSnackbar('更新失敗','error')
        console.log(err);
      });
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid item xs={12}></Grid>
      <Button type="submit">参加する</Button>
    </Box>
  );
};

const ConvertModalField: React.FC<BidderModalProps> = (
  props: BidderModalProps
) => {
  const {showSnackbar}=useSnackbar()
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    axios
      .patch(`/bids/${props.data.id}/convert`, {
        user_id: props.data.user_id,
      })
      .then((response) => {
        showSnackbar('更新成功','success')
        console.log(response);
      })
      .catch((err) => {
        showSnackbar('更新失敗','error')
        console.log(err);
      });
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid item xs={12}></Grid>
      <Button type="submit">交代する</Button>
    </Box>
  );
};

const CheckWorkModalField: React.FC<ResponseCardProps<SlotResponse>> = (
  props: ResponseCardProps<SlotResponse>
) => {
  const {showSnackbar}=useSnackbar()
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    axios
      .post(`/slots/${props.data.id}/complete`)
      .then((response) => {
        showSnackbar('更新成功','success')
        console.log(response);
      })
      .catch((err) => {
        showSnackbar('更新失敗','error')
        console.log(err);
      });
  };

  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid item xs={12}></Grid>
      <Button type="submit">仕事をしました</Button>
    </Box>
  );
};

const SlotModalField: React.FC<ResponseCardProps<SlotResponse>> = (
  props: ResponseCardProps<SlotResponse>
) => {
  const {showSnackbar}=useSnackbar()
  const start_time_string = `${props.data.start_time.year}-${props.data.start_time.month}-${props.data.start_time.day}`;
  const end_time_string = `${props.data.end_time.year}-${props.data.end_time.month}-${props.data.end_time.day}`;
  const [starttime, setStarttime] = React.useState<Dayjs | null>(
    dayjs(start_time_string)
  );
  const [endtime, setEndtime] = React.useState<Dayjs | null>(
    dayjs(end_time_string)
  );
  const [id, setID] = React.useState<string>(props.data.task.id);
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .patch(`/slots/${props.data.id}`, {
        name: data.get("name"),
        start_time: {
          year: starttime ? starttime.get("year") : props.data.start_time.year,
          month: starttime
            ? starttime.get("month") + 1
            : props.data.start_time.month,
          day: starttime ? starttime.get("day") : props.data.start_time.day,
          hour: starttime ? starttime.get("hour") : props.data.start_time.hour,
          minute: starttime
            ? starttime.get("minute")
            : props.data.start_time.minute,
        },
        end_time: {
          year: endtime ? endtime.get("year") : props.data.end_time.year,
          month: endtime ? endtime.get("month") + 1 : props.data.end_time.month,
          day: endtime ? endtime.get("day") : props.data.end_time.day,
          hour: endtime ? endtime.get("hour") : props.data.end_time.hour,
          minute: endtime ? endtime.get("minute") : props.data.end_time.minute,
        },
        task: id,
      })
      .then((response) => {
        console.log(response);
        showSnackbar('更新成功','success')
      })
      .catch((err) => {
        showSnackbar('更新失敗','error')
        console.log(err);
      });
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField
            autoComplete="given-name"
            name="name"
            required
            fullWidth
            id="name"
            label="名前"
            defaultValue={props.data.name}
            autoFocus
          />
        </Grid>
        <Grid item xs={12} sm={6}>
          <DateSelect
            title="集合時刻"
            date={starttime}
            setValue={setStarttime}
            setOther={{ setOther: setEndtime, timedelta: 1, unit: "h" }}
          />
        </Grid>
        <Grid item xs={12}>
          <DateSelect
            title="終了予定時刻"
            date={endtime}
            setValue={setEndtime}
          />
        </Grid>
        <Grid>
          <SingleChoiceField
            url="/tasks/"
            title="タスク"
            id={id}
            setData={setID}
          />
        </Grid>
      </Grid>
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        情報を更新
      </Button>
    </Box>
  );
};

const TaskModalField: React.FC<ResponseCardProps<TaskResponse>> = (
  props: ResponseCardProps<TaskResponse>
) => {
  const {showSnackbar}=useSnackbar()
  const [tag_id, setTagID] = React.useState<string[]>([]);
  const [auth_id, setAuthID] = React.useState<string[]>([]);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .patch(`/tasks/${props.data.id}`, {
        name: data.get("name"),
        detail: data.get("detail"),
        max_woker_num: data.get("max_woker_num"),
        min_woker_num: data.get("min_woker_num"),
        exp_woker_num: data.get("exp_woker_num"),
        tag: tag_id,
        authority: auth_id,
      })
      .then((response) => {
        console.log(response);
        showSnackbar('更新成功','success')


      })
      .catch((err) => {
        showSnackbar('更新失敗','error')
        console.log(err);
      });
  };
  return (
    <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <TextField
            autoComplete="given-name"
            name="name"
            required
            fullWidth
            id="name"
            defaultValue={props.data.name}
            label="名前"
            autoFocus
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            name="detail"
            maxRows={10}
            required
            id="detail"
            label="説明"
            fullWidth
            margin="normal"
            multiline
            variant="outlined"
            placeholder="400字以内"
            defaultValue={props.data.detail}
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="max_woker_num"
            name="max_woker_num"
            inputProps={{ min: "1", step: "1" }}
            label="最大人数"
            defaultValue={props.data.max_worker_num}
            type="number"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="min_woker_num"
            name="min_woker_num"
            inputProps={{ min: "1", step: "1" }}
            label="最小人数"
            defaultValue={props.data.min_worker_num}
            type="number"
          />
        </Grid>
        <Grid item xs={12}>
          <TextField
            id="exp_woker_num"
            name="exp_woker_num"
            inputProps={{ min: "0", step: "1" }}
            label="必要な経験者の人数"
            defaultValue={props.data.exp_worker_num}
            type="number"
          />
        </Grid>
        <Grid>
          <SimpleChoiceField
            url="/tags"
            title="タグ"
            id={tag_id}
            setData={setTagID}
          />
        </Grid>
        <Grid>
          <SimpleChoiceField
            url="/authority"
            title="権限"
            id={auth_id}
            setData={setAuthID}
          />
        </Grid>
      </Grid>
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        新規作成
      </Button>
    </Box>
  );
};

export const ResponseDisplay: React.FC<ResponseDisplayProps> = (
  props: ResponseDisplayProps
) => {

  const value = React.useContext(TabContext)
  if (value===0 && isSlot(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="left">
    <p>{props.data.start_time.hour}時{props.data.start_time.minute}分開始</p>
    <p>{props.data.end_time.hour}時{props.data.end_time.minute}分終了</p>
  </Typography>
    );
  } else if (value===1 && isBid(props.data)) {
    return (<>
      <Typography variant="body2" color="text.secondary" align="right">
        <p>{props.data.slot.start_time.hour}時{props.data.slot.start_time.minute}
        分開始</p> <p>回答締め切り:{props.data.close_time.month}月
        {props.data.close_time.day}日</p>
      </Typography>{
        props.data.user_bidpoint!=='notyet' ?(<Typography variant="body2" color='success' align='center'>
          入札済み:{props.data.user_bidpoint}
        </Typography>):(<></>)
      }
      </>
    );
  } else if (value === 2 && isBidder(props.data)){
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        <p>交代申請者{props.data.user}</p>
        <p>交代したい仕事{props.data.name}</p>
        <p>交代して貰えるポイント{props.data.point}</p>
      </Typography>
    );
  } else if ((value===3||value===4) && isBid(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        <p>{props.data.slot.start_time.hour}時{props.data.slot.start_time.minute}分開始</p>
        <p>{props.data.slot.end_time.hour}時{props.data.slot.end_time.minute}分終了</p>
        <p>貰えるポイント：{props.data.buyout_point-1}</p>
      </Typography>
    );
  } else if (value===5 && isSlot(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        <p>貰えるポイント：{props.data.name}</p>
      </Typography>
    );
  } else if (value===6 && isSlot(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="left">
    <p>{props.data.start_time.hour}時{props.data.start_time.minute}分開始</p>
    <p>{props.data.end_time.hour}時{props.data.end_time.minute}分終了</p>
  </Typography>
    );
  } else if (value===7 && isTask(props.data)) {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        <p>最低限必要な人数:{props.data.min_worker_num}人</p> <p>その中で必要な経験者の数:
        {props.data.exp_worker_num}人</p> <p>最大人数:{props.data.max_worker_num}人</p>
      </Typography>
    );
  } else {
    return (
      <Typography variant="body2" color="text.secondary" align="right">
        表示できる情報はありません
      </Typography>
    );
  }
};

export const isBid = (data: any): data is BidResponse => {
  return !!(data as BidResponse)?.open_time;
};

export const isSlot = (data: any): data is SlotResponse => {
  return !!(data as SlotResponse)?.start_time;
};

export const isTask = (data: any): data is TaskResponse => {
  return !!(data as TaskResponse)?.exp_worker_num;
};

export const isBidder = (data: any): data is BidderResponse => {
  return (
    !!(data as BidderResponse)?.point && !!(data as BidderResponse)?.user_id
  );
};
