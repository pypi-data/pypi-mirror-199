import React from 'react';

import Paper from '@material-ui/core/Paper';
import MenuList from '@material-ui/core/MenuList';
import MenuItem from '@material-ui/core/MenuItem';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import Typography from '@material-ui/core/Typography';
import FiberNewIcon from '@material-ui/icons/FiberNew';
import FileCopyIcon from '@material-ui/icons/FileCopy';
import { Button, Menu, Tooltip } from '@material-ui/core';
import MenuIcon from '@material-ui/icons/Menu';
import FormDialog from '../General/FormDialog';
import type {
  EwoksRFLink,
  EwoksRFNode,
  GraphDetails,
  GraphRF,
  Task,
} from '../../types';
import state from '../../store/state';

export default function IconMenu() {
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const open = Boolean(anchorEl);
  const [openSaveDialog, setOpenSaveDialog] = React.useState<boolean>(false);
  const [elementToEdit, setElementToEdit] = React.useState<Task | GraphRF>({});
  const [doAction, setDoAction] = React.useState<string>('');
  const selectedElement = state<EwoksRFNode | EwoksRFLink | GraphDetails>(
    (state) => state.selectedElement
  );
  const initializedTask = state((state) => state.initializedTask);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);

  const graphRF = state((state) => state.graphRF);
  const tasks = state((state) => state.tasks);

  function handleClick(event: React.MouseEvent<HTMLButtonElement>) {
    setAnchorEl(event.currentTarget);
  }

  function handleClose() {
    setAnchorEl(null);
  }

  function action(
    action: string,
    element: Task | EwoksRFNode | EwoksRFLink | GraphRF
  ) {
    setDoAction(action);
    if (action === 'newTask') {
      setElementToEdit(initializedTask);
    } else if (action === 'cloneTask') {
      if ('position' in element) {
        if (element.task_type === 'graph') {
          setOpenSnackbar({
            open: true,
            text: 'Cannot clone a graph, please select a Task!',
            severity: 'warning',
          });
          return;
        }
        // DOC: if the task does not exist in the tasks populate the form with the element details
        const task = tasks.find(
          (tas) => tas.task_identifier === element.task_identifier
        );

        setElementToEdit(
          task || {
            ...initializedTask,
            task_identifier: element.task_identifier,
            task_type: element.task_type,
          }
        );
      } else {
        setOpenSnackbar({
          open: true,
          text: 'First select in the canvas a Node to clone and Save as Task',
          severity: 'warning',
        });
        return;
      }
    } else if (action === 'cloneGraph') {
      setElementToEdit(graphRF);
    }

    setOpenSaveDialog(true);
  }

  return (
    <>
      <FormDialog
        elementToEdit={elementToEdit}
        action={doAction}
        open={openSaveDialog}
        setOpenSaveDialog={setOpenSaveDialog}
      />
      <Tooltip title="Clone or create task/workflow" arrow>
        <Button
          style={{ margin: '8px' }}
          variant="contained"
          color="primary"
          onClick={handleClick}
          size="small"
          data-cy="iconMenu"
        >
          <MenuIcon />
        </Button>
      </Tooltip>
      <Menu
        id="basic-menu"
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        MenuListProps={{
          'aria-labelledby': 'basic-button',
        }}
      >
        <Paper>
          <MenuList>
            <MenuItem onClick={() => action('newTask', initializedTask)}>
              <ListItemIcon>
                <FiberNewIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>New Task</ListItemText>
            </MenuItem>
            <MenuItem onClick={() => action('cloneTask', selectedElement)}>
              <ListItemIcon>
                <FileCopyIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Clone as Task</ListItemText>
            </MenuItem>
            <MenuItem onClick={() => action('cloneGraph', graphRF)}>
              <ListItemIcon>
                <FileCopyIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText>Clone Graph</ListItemText>
              <Typography variant="body2" color="primary" />
            </MenuItem>
          </MenuList>
        </Paper>
      </Menu>
    </>
  );
}
