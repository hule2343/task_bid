import * as React from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import axios from '../axios';

export const AdminPage:React.FC=()=> {
    const handleClick = () => {
        axios.post('/admin/closebid').then(
            (response) => {
                console.log(response.data)
            }
        ).catch((err) => {
            console.log(err)
        })
    }
  return (
    <Stack spacing={2} direction="row">
      <Button variant="text" onClick={handleClick}>Close Finished Bids</Button>
      <Button variant="contained">Contained</Button>
      <Button variant="outlined">Outlined</Button>
    </Stack>
  );
}
