import React, { useEffect } from 'react';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import { Box } from '@material-ui/core';

import ManageIcons from './ManageIcons';
import ManageWorkflows from './ManageWorkflows';
import ManageTasks from './ManageTasks';
import { getIcons } from '../../utils/api';
import ExecutionTable from '../Execution/ExecutionTable';
import state from '../../store/state';

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
          <Typography component="span">{children}</Typography>
        </Box>
      )}
    </div>
  );
}

function a11yProps(index: number) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

export default function BasicTabs() {
  const [value, setValue] = React.useState(0);
  const openSettingsDrawer = state((state) => state.openSettingsDrawer);

  useEffect(() => {
    setValue(
      openSettingsDrawer === 'Workflows'
        ? 0
        : openSettingsDrawer === 'Tasks'
        ? 1
        : openSettingsDrawer === 'Icons'
        ? 2
        : openSettingsDrawer === 'Executions'
        ? 3
        : openSettingsDrawer === 'Settings'
        ? 4
        : 0
    );
  }, [openSettingsDrawer]);

  const handleChange = async (
    event: React.SyntheticEvent,
    newValue: number
  ) => {
    setValue(newValue);
    if (newValue === 2) {
      await getIcons();
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs
          value={value}
          onChange={handleChange}
          aria-label="basic tabs example"
        >
          <Tab label="Workflows" {...a11yProps(0)} />
          <Tab label="Tasks" {...a11yProps(1)} />
          <Tab label="Icons" {...a11yProps(2)} />
          <Tab label="Executions" {...a11yProps(3)} />
          {/* <Tab label="Settings" {...a11yProps(4)} /> */}
        </Tabs>
      </Box>
      <TabPanel value={value} index={0}>
        <ManageWorkflows />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <ManageTasks />
      </TabPanel>
      <TabPanel value={value} index={2}>
        <ManageIcons />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <ExecutionTable />
      </TabPanel>
    </Box>
  );
}
