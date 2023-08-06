import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Paper from '@material-ui/core/Paper';
import FiberNew from '@material-ui/icons/FiberNew';
import ImportContactsIcon from '@material-ui/icons/ImportContacts';
import Sidebar from 'Components/Sidebar/Sidebar';
import { ReactFlowProvider } from 'react-flow-renderer';
import { Link } from 'react-router-dom';
import Canvas from '../Components/Canvas/Canvas';
import UndoRedo from '../Components/TopNavBar/UndoRedo';
import GetFromServer from '../Components/General/GetFromServer';
import { Fab, IconButton, Typography } from '@material-ui/core';
import SettingsIcon from '@material-ui/icons/Settings';
import SimpleSnackbar from '../Components/General/Snackbar';
import SettingsInfoDrawer from '../Components/TopNavBar/SettingsInfoDrawer';
import SubgraphsStack from '../Components/TopNavBar/SubgraphsStack';
import LinearSpinner from '../Components/General/LinearSpinner';
import ExecuteWorkflow from '../Components/Execution/ExecuteWorkflow';
import Tooltip from '@material-ui/core/Tooltip';
import DashboardStyle from './DashboardStyle';
import SaveToServer from '../Components/TopNavBar/SaveToServer';
import tooltipText from '../Components/General/TooltipText';
import state from '../store/state';
import NotListedLocationIcon from '@material-ui/icons/NotListedLocation';
import FormDialog from '../Components/General/FormDialog';
import ConfirmDialog from 'Components/General/ConfirmDialog';
import { ErrorBoundary } from 'react-error-boundary';
import ErrorFallback from '../Components/General/ErrorFallback';
import MenuPopover from '../Components/General/MenuPopover';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import { ReflexContainer, ReflexSplitter, ReflexElement } from 'react-reflex';

const useStyles = DashboardStyle;

export default function Dashboard() {
  const classes = useStyles();

  const undoF = React.useRef(null);
  const redoF = React.useRef(null);
  const saveToServerF = React.useRef(null);

  const [openDrawers, setOpenDrawers] = useState(true);
  const [openSettings, setOpenSettings] = useState(false);
  const [openInfo, setOpenInfo] = useState(false);
  const gettingFromServer = state((state) => state.gettingFromServer);
  const inExecutionMode = state((state) => state.inExecutionMode);
  const graphRF = state((state) => state.graphRF);
  const [openSaveDialog, setOpenSaveDialog] = useState<boolean>(false);
  const openSettingsDrawer = state((state) => state.openSettingsDrawer);
  const setOpenSettingsDrawer = state((state) => state.setOpenSettingsDrawer);
  const canvasGraphChanged = state((state) => state.canvasGraphChanged);
  const setCanvasGraphChanged = state((state) => state.setCanvasGraphChanged);
  const [openAgreeDialog, setOpenAgreeDialog] = useState<boolean>(false);
  const undoIndex = state((state) => state.undoIndex);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  useEffect(() => {
    handleOpenInfo();
  }, []);

  useEffect(() => {
    if (!openDrawers) {
      setOpenSettings(false);
      setOpenSettingsDrawer('Workflows');
    }
  }, [openDrawers, openSettings, setOpenSettingsDrawer]);

  useEffect(() => {
    if (openSettingsDrawer === 'Executions') {
      setOpenInfo(false);
      setOpenDrawers(true);
      setOpenSettings(true);
    } else if (openSettingsDrawer === 'close') {
      setOpenInfo(false);
      setOpenDrawers(false);
      setOpenSettings(false);
    }
  }, [openSettingsDrawer, setOpenSettingsDrawer]);

  const checkAndNewGraph = () => {
    if (canvasGraphChanged && undoIndex !== 0) {
      setOpenAgreeDialog(true);
    } else {
      setOpenSaveDialog(true);
      setOpenAgreeDialog(false);
      setCanvasGraphChanged(false);
    }
  };

  const openGraph = () => {
    handleOpenSettings();
  };

  const handleOpenSettings = () => {
    setOpenInfo(false);
    setOpenSettings(true);
    setOpenDrawers(true);
  };
  const handleOpenDrawers = () => {
    setOpenDrawers(!openDrawers);
  };

  const handleOpenInfo = () => {
    setOpenSettings(false);
  };

  const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);

  function handleKeyDown(event) {
    const charCode = String.fromCharCode(event.which).toLowerCase();

    const keys = event.ctrlKey || event.metaKey;
    if (keys && charCode === 's') {
      event.preventDefault();
      event.stopPropagation();
      saveToServerF.current();
    } else if (keys && charCode === 'z') {
      event.preventDefault();
      event.stopPropagation();
      undoF.current();
    } else if (keys && charCode === 'y') {
      event.preventDefault();
      event.stopPropagation();
      redoF.current();
    } else if (keys && event.shiftKey && charCode === 'n') {
      event.preventDefault();
      event.stopPropagation();
      checkAndNewGraph();
    }
  }

  const disAgreeSaveWithout = () => {
    setOpenAgreeDialog(false);
  };

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <div
      className={classes.root}
      onKeyDown={handleKeyDown}
      tabIndex={0}
      role="button"
    >
      <ConfirmDialog
        title="There are unsaved changes"
        content="Continue without saving?"
        open={openAgreeDialog}
        agreeCallback={checkAndNewGraph}
        disagreeCallback={disAgreeSaveWithout}
      />
      <FormDialog
        elementToEdit={graphRF}
        action="cloneGraph"
        open={openSaveDialog}
        setOpenSaveDialog={setOpenSaveDialog}
      />
      <CssBaseline />
      <SimpleSnackbar />
      <AppBar
        position="absolute"
        className={clsx(classes.appBar, classes.appBarShift)}
        style={{ height: '5%', minHeight: '64px' }}
      >
        <Toolbar className={classes.toolbar}>
          <SubgraphsStack />
          <Tooltip
            title={tooltipText('Start a new workflow')}
            enterDelay={800}
            arrow
          >
            <IconButton
              color="inherit"
              onClick={checkAndNewGraph}
              disabled={inExecutionMode}
            >
              <Fab
                className={classes.openFileButton}
                color="primary"
                size="small"
                component="span"
                aria-label="add"
                disabled={inExecutionMode}
              >
                <FiberNew />
              </Fab>
            </IconButton>
          </Tooltip>
          <Tooltip
            title={tooltipText('Open an existing workflow')}
            enterDelay={800}
            arrow
          >
            <IconButton
              color="inherit"
              onClick={openGraph}
              disabled={inExecutionMode}
            >
              <Fab
                className={classes.openFileButton}
                color="primary"
                size="small"
                component="span"
                aria-label="add"
                disabled={inExecutionMode}
              >
                <ImportContactsIcon />
              </Fab>
            </IconButton>
          </Tooltip>
          <div className={classes.verticalRule} />
          <UndoRedo undoF={undoF} redoF={redoF} />
          <div className={classes.verticalRule} />
          <SaveToServer saveToServerF={saveToServerF} />
          <GetFromServer />
          <ExecuteWorkflow />
          <div>
            <Tooltip title={tooltipText('More')} enterDelay={800} arrow>
              <IconButton color="inherit" onClick={handleClick}>
                <Fab
                  className={classes.openFileButton}
                  color="primary"
                  size="small"
                  component="span"
                  aria-label="add"
                >
                  <MoreVertIcon />
                </Fab>
              </IconButton>
            </Tooltip>
            <MenuPopover anchorEl={anchorEl} handleClose={handleClose} />
          </div>
          <div className={classes.verticalRule} />
          <Tooltip
            title={tooltipText('Manage tasks, icons and workflows')}
            enterDelay={800}
            arrow
          >
            <IconButton color="inherit" onClick={handleOpenSettings}>
              <Fab
                className={classes.openFileButton}
                color="primary"
                size="small"
                component="span"
                aria-label="add"
              >
                <SettingsIcon />
              </Fab>
            </IconButton>
          </Tooltip>

          <Tooltip
            title={tooltipText('Guide for Ewoks UI')}
            enterDelay={800}
            arrow
          >
            <IconButton color="inherit">
              <Typography
                component="h1"
                variant="h5"
                color="primary"
                style={{ padding: '5px' }}
              >
                <Link to="/">
                  <Fab
                    className={classes.openFileButton}
                    color="primary"
                    size="small"
                    component="span"
                    aria-label="add"
                  >
                    <NotListedLocationIcon />
                  </Fab>
                </Link>
              </Typography>
            </IconButton>
          </Tooltip>
          <SettingsInfoDrawer
            handleOpenDrawers={handleOpenDrawers}
            openDrawers={openDrawers}
            openInfo={openInfo}
            openSettings={openSettings}
          />
        </Toolbar>
      </AppBar>

      <ReflexContainer
        orientation="vertical"
        style={{
          flex: '1 4 0%',
          display: 'flex',
          minWidth: 0,
        }}
      >
        <ReflexElement
          className="left-pane"
          minSize={100}
          maxSize={500}
          size={350}
        >
          <Sidebar />
        </ReflexElement>
        <ReflexSplitter
          propagate
          style={{
            display: 'flex',
            alignItems: 'center',
            width: '0.325rem',
            height: '100vh',
            backgroundColor: 'rgb(233, 235, 247)',
            borderRight: 'none !important',
            borderLeftColor: '#eee !important',
            color: '#777',
            cursor: 'col-resize',
            transition: 'none',
          }}
        />
        <ReflexElement className="right-pane">
          <main className={classes.content}>
            <div className={classes.toolbar} />

            <Paper className={fixedHeightPaper}>
              {gettingFromServer && <LinearSpinner />}

              <ReactFlowProvider>
                <ErrorBoundary
                  FallbackComponent={(fallbackProps) => (
                    <ErrorFallback {...fallbackProps} />
                  )}
                >
                  <Canvas />
                </ErrorBoundary>
              </ReactFlowProvider>
            </Paper>
          </main>
        </ReflexElement>
      </ReflexContainer>
    </div>
  );
}
