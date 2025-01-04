import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HelpIcon from '@mui/icons-material/Help';
import SettingsIcon from '@mui/icons-material/Settings';
import LogoutIcon from '@mui/icons-material/Logout';
import TelegramIcon from '@mui/icons-material/Telegram';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import Box from '@mui/material/Box';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';
import Drawer from '@mui/material/Drawer';
import Button from '@mui/material/Button';
import MenuIcon from '@mui/icons-material/Menu';
import HomeIcon from '@mui/icons-material/Home';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';

export default function DrawerComponent () {

    const navigate = useNavigate();

    const [open, setOpen] = useState(false);
    
    const isHomePage = window.location.pathname === "/home";

    const toggleDrawer = (open) => (event) => {
        if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
        return;
        }
        setOpen(open);
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
      };
    
      const handleHelp = () => {
        navigate('/help');
      };
    
      const handleSettings = () => {
        navigate('/settings');
      };

      const handleBudget = () => {
        navigate('/budget')
      }
    
      const handleTelegram = () => {
        navigate('/telegram');
      };
    
      const handleFunctions = () => {
        navigate('/functions');
      };

      const handleHomePage = () => {
        navigate('/home');
      }

    const DrawerList = () => (
        <Box sx={{ width: 250, zIndex: 99999999 }} role="presentation">
          <List>
          {!isHomePage && 
            <ListItem key="HomePage" disablePadding>
              <ListItemButton onClick={() => handleHomePage()}>
                <ListItemIcon>
                  <HomeIcon />
                </ListItemIcon>
                <ListItemText primary="HomePage"/>
              </ListItemButton>
            </ListItem>
            
            }
            <Divider />
          {/* <ListItem key="MyFunctions" disablePadding>
              <ListItemButton onClick={() => handleFunctions()}>
                <ListItemIcon>
                  <AnalyticsIcon />
                </ListItemIcon>
                <ListItemText primary="MyFunctions"/>
              </ListItemButton>
            </ListItem>
            <ListItem key="Telegram Bot" disablePadding>
              <ListItemButton onClick={() => handleTelegram()}>
                <ListItemIcon>
                  <TelegramIcon />
                </ListItemIcon>
                <ListItemText primary="Telegram Bot"/>
              </ListItemButton>
            </ListItem>
          <Divider />
            <ListItem key="Help" disablePadding>
              <ListItemButton onClick={() => handleHelp()}>
                <ListItemIcon>
                  <HelpIcon />
                </ListItemIcon>
                <ListItemText primary="Help" />
              </ListItemButton>
            </ListItem> */}
    
            <ListItem key="Settings" disablePadding>
              <ListItemButton onClick={() => handleSettings()}>
                <ListItemIcon>
                  <SettingsIcon />
                </ListItemIcon>
                <ListItemText primary="Settings" />
              </ListItemButton>
            </ListItem>

            <ListItem key="Budget" disablePadding>
              <ListItemButton onClick={() => handleBudget()}>
                <ListItemIcon>
                  <AttachMoneyIcon />
                </ListItemIcon>
                <ListItemText primary="Budget" />
              </ListItemButton>
            </ListItem>
          </List>
          <Divider />
          <List>
              <ListItem key={"Logout"} disablePadding>
                <ListItemButton onClick={() => handleLogout()}>
                  <ListItemIcon>
                  <LogoutIcon />
                  </ListItemIcon>
                  <ListItemText primary={"Logout"} />
                </ListItemButton>
              </ListItem>
          </List>
        </Box>
      );

    return (
        <div style={{position: 'absolute', top: 0, right: 0, width: "10%", height: "100%", zIndex: 99}}>
        
        <Button onClick={toggleDrawer(true)} sx={{width: "100%", height: "100%", position: 'absolute', top: 0, right: 0}}>
          <MenuIcon sx={{width: "50%", height: "50%", color: "white"}}/>
        </Button>
        <Drawer open={open} onClose={toggleDrawer(false)} anchor='right' sx={{zIndex: 999999}}>
          <DrawerList />
        </Drawer>
      </div>
    )
}