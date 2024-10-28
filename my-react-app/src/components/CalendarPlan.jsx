import * as React from 'react';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import AppBarComponent from './AppBarComponent';
import BudgetTable from './BudgetTableComponent';
import { Box } from '@mui/material';

export default function FirstComponent() {
  const [from_value, setValue] = React.useState();
  const [to_value, setToValue] = React.useState();

  return (
    <div>
    
    <BudgetTable/>
    <AppBarComponent/>
    <Box>
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DatePicker />
    </LocalizationProvider>
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <DatePicker />
    </LocalizationProvider>
    </Box>
    </div>
  );
}