// /* eslint-disable sonarjs/cognitive-complexity */
import React, { useEffect, useState } from 'react';
import ReactJson from 'react-json-view';
import PlayCircleOutlineIcon from '@material-ui/icons/PlayCircleOutline';
import IntegratedSpinner from '../General/IntegratedSpinner';
import state from '../../store/state';
import { Button, Chip, IconButton } from '@material-ui/core';
import type { Event, GraphEwoks, WorkflowDescription } from '../../types';
import { getWorkflow } from '../../utils/api';
import DeleteIcon from '@material-ui/icons/Delete';
import ConfirmDialog from 'Components/General/ConfirmDialog';

export default function ExecutionDetails() {
  // const graphRF = state((state) => state.graphRF);

  const currentExecutionEvent = state((state) => state.currentExecutionEvent);

  // DOC: events from the ongoing live executions
  const executedEvents = state((state) => state.executedEvents);

  // DOC: the workflows from HISTORY that are visible on the execution tab
  const watchedWorkflows = state((state) => state.watchedWorkflows);
  const setWatchedWorkflows = state((state) => state.setWatchedWorkflows);

  // DOC: all workflows live and from history on the execution tab
  const [workflows, setWorkflows] = useState([]);

  // DOC: calculate the executing spinners for live execution
  const setExecutingEvents = state((state) => state.setExecutingEvents);
  // const executingEvents = state((state) => state.executingEvents);

  const setInExecutionMode = state((state) => state.setInExecutionMode);

  // DOC: the events that are each moment on the canvas NOT? for live executing workflows
  const [currentWatchedEvents, setCurrentWatchedEvents] = useState(
    [] as Event[]
  );
  // const [jobs, setJobs] = useState([]);

  const [selectedWorkflow, setSelectedWorkflow] = useState<Event>({} as Event);

  // const [gettingFromServer, setGettingFromServer] = useState(false); TODO: Use the global...
  const setGettingFromServer = state((state) => state.setGettingFromServer);
  const gettingFromServer = state((state) => state.gettingFromServer);

  const setWorkingGraph = state((state) => state.setWorkingGraph);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const allWorkflows = state((state) => state.allWorkflows);

  // const [expandedWorkflows, setExpandedWorkflows] = useState<boolean>(false);
  // const openSettingsDrawer = state((state) => state.openSettingsDrawer);
  const setOpenSettingsDrawer = state((state) => state.setOpenSettingsDrawer);
  const setCanvasGraphChanged = state((state) => state.setCanvasGraphChanged);
  const [openAgreeDialog, setOpenAgreeDialog] = useState<boolean>(false);
  const undoIndex = state((state) => state.undoIndex);
  const canvasGraphChanged = state((state) => state.canvasGraphChanged);

  useEffect(() => {
    // DOC: for those live executing search the executedEvents
    const allWorkflowsL = executedEvents
      .filter((ev) => ev.context === 'workflow' && ev.type === 'start')
      .map((work) => {
        let workL = {};
        if (
          executedEvents.some(
            (wor) =>
              wor.workflow_id === work.workflow_id &&
              wor.context === 'workflow' &&
              wor.type === 'end'
          )
        ) {
          workL = { ...work, status: 'finished' };
        } else {
          workL = { ...work, status: 'executing' };
        }
        return workL;
      });

    const wjobs = watchedWorkflows.map((job) => {
      return { ...(job[0].workflow_id ? job[0] : job[1]), status: 'finished' };
    });

    setWorkflows([...allWorkflowsL, ...wjobs]);
  }, [executedEvents, watchedWorkflows]);

  function workflowDetails(work) {
    if (selectedWorkflow !== work) {
      setSelectedWorkflow(work);
    } else {
      setSelectedWorkflow({} as Event);
    }
  }

  function formatedDate(job: Event) {
    const allWorkF: WorkflowDescription[] = [
      ...(allWorkflows as WorkflowDescription[]),
    ];

    const { label } = (allWorkF &&
      allWorkF.find((work) => job.workflow_id === work.id)) || {
      label: '',
    };
    const dat = new Date(job.time);

    return `${
      label ? label.slice(0, 20) : job.workflow_id
    } ${dat.getHours()}:${dat.getMinutes()} ${dat.getDate()}/${
      dat.getMonth() + 1
    }/${dat.getFullYear()}`;
  }

  function checkAndExecute() {
    if (canvasGraphChanged && undoIndex !== 0) {
      setOpenAgreeDialog(true);
    } else {
      executeWorkflow();
      setOpenAgreeDialog(false);
      setCanvasGraphChanged(false);
    }
  }

  async function executeWorkflow() {
    // DOC: need to differentiate between the live-executing, live-executed, jobs-from-server
    setInExecutionMode(true);

    const workflowId = selectedWorkflow.workflow_id;
    // DOC: Replay execution on canvas needs to put the workflow on canvas with
    // the events if not there
    // if (graphRF.graph.id !== workflowId) {
    // DOC: Get the workflow from server if not on canvas
    // TODO: dublicated code with getFromServer, abstract in store? hook?
    setGettingFromServer(true);
    try {
      const response = await getWorkflow(workflowId);
      if (response.data) {
        setWorkingGraph(response.data as GraphEwoks, 'fromServer');
        // TODO: get rid of timeout?
        setTimeout(() => {
          // DOC:
          const events = getEventsForJob();

          // TODO: timeout is needed because executingEvents try to find
          // the nodes before they are there from the server
          // probably because setWorkingGraph changes the graphRF used in executingEvents
          events.forEach((ev) => setExecutingEvents(ev, false));
        }, 400);
      } else {
        setOpenSnackbar({
          open: true,
          text: 'Could not locate the requested workflow! Maybe it is deleted!',
          severity: 'warning',
        });
      }
    } catch (error) {
      setOpenSnackbar({
        open: true,
        text:
          error.response?.data?.message ||
          'Error in retrieving workflow. Please check connectivity with the server!',
        severity: 'error',
      });
    } finally {
      setGettingFromServer(false);
    }
  }

  function getEventsForJob() {
    let events = [] as Event[];
    const isInWatchedIndex = watchedWorkflows
      .map((job) => job[0].job_id === selectedWorkflow.job_id)
      .indexOf(true);

    // Check if it is watched workflow from server or a live execution
    if (isInWatchedIndex !== -1) {
      events = watchedWorkflows[isInWatchedIndex].map((ev, index) => {
        return { ...ev, id: index + 1 };
      });
    } else {
      events = executedEvents.filter(
        (ev) =>
          ev.workflow_id === selectedWorkflow.workflow_id &&
          ev.job_id === selectedWorkflow.job_id
      );
    }
    setCurrentWatchedEvents(events);
    return events;
  }

  async function handleChangeOpenExecutions() {
    setOpenSettingsDrawer('Executions');
  }

  function handleChangeCleanExecutions() {
    setWorkflows([]);
  }

  function deleteWatchedJob() {
    setWorkflows(
      workflows.filter((work) => work.job_id !== selectedWorkflow.job_id)
    );

    setWatchedWorkflows(
      watchedWorkflows.filter(
        (work) => work[0].job_id !== selectedWorkflow.job_id
      )
    );
  }

  function disAgreeExecuteWithout() {
    setOpenAgreeDialog(false);
  }

  return (
    <>
      {workflows.map((work) => (
        <div
          key={work.time}
          style={{
            backgroundColor:
              work.status === 'finished' ? '#b6beec' : 'rgb(124, 163, 198)',
            borderRadius: '5px',
            margin: '2px',
            width: '98%',
          }}
        >
          <div
            style={{
              display: 'block',
              paddingTop: '5px',
              paddingBottom: '5px',
            }}
          >
            <Chip
              label={formatedDate(work)}
              onClick={() => workflowDetails(work)}
              style={{
                paddingTop: '5px',
                paddingBottom: '5px',
                backgroundColor: '#e9ebf7',
                width: '98%',
              }}
              size="medium"
              // variant="outlined"
            />
          </div>
          {selectedWorkflow.job_id === work.job_id && (
            <div style={{ display: 'flex', width: '98%' }}>
              <ReactJson
                src={work}
                name="Execution details"
                theme="monokai"
                collapsed
                collapseStringsAfterLength={25}
                groupArraysAfterLength={15}
                enableClipboard={false}
                quotesOnKeys={false}
                style={{
                  backgroundColor: 'rgb(59, 77, 172)',
                  margin: '7px',
                  width: '98%',
                }}
                displayDataTypes={false}
              />
            </div>
          )}
          {selectedWorkflow.job_id === work.job_id && (
            <span style={{ display: 'flex' }}>
              <ConfirmDialog
                title="There are unsaved changes"
                content="Continue without saving?"
                open={openAgreeDialog}
                agreeCallback={executeWorkflow}
                disagreeCallback={disAgreeExecuteWithout}
              />
              <IntegratedSpinner
                getting={gettingFromServer}
                tooltip="Execute Workflow and exit Execution mode"
                action={checkAndExecute}
                onClick={() => {
                  // Keep logging in console for debugging when talking with a user
                  /* eslint-disable no-console */
                  console.log('Starting Execution');
                }}
              >
                <PlayCircleOutlineIcon fontSize="large" />
              </IntegratedSpinner>
              <IconButton
                onClick={deleteWatchedJob}
                aria-label="delete"
                color="primary"
              >
                <DeleteIcon />
              </IconButton>
            </span>
          )}
        </div>
      ))}
      <Button
        color="primary"
        onClick={handleChangeOpenExecutions}
        variant="outlined"
        size="small"
      >
        All Executions
      </Button>
      <Button
        color="secondary"
        onClick={handleChangeCleanExecutions}
        variant="outlined"
        size="small"
      >
        Clean all
      </Button>
      {currentWatchedEvents[currentExecutionEvent - 1] && (
        <ReactJson
          src={currentWatchedEvents[currentExecutionEvent - 1]}
          name="Event details"
          theme="monokai"
          collapsed
          collapseStringsAfterLength={20}
          groupArraysAfterLength={15}
          enableClipboard={false}
          quotesOnKeys={false}
          style={{ backgroundColor: 'rgb(59, 77, 172)' }}
          displayDataTypes={false}
        />
      )}
    </>
  );
}
