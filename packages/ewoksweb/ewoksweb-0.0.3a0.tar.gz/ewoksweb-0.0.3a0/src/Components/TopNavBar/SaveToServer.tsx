import { useState, useEffect } from 'react';
import IntegratedSpinner from '../General/IntegratedSpinner';
import { rfToEwoks } from '../../utils';
import CloudUploadIcon from '@material-ui/icons/CloudUpload';
import state from '../../store/state';
import configData from '../../configData.json';
import FormDialog from '../General/FormDialog';
import curateGraph from './utils/curateGraph';
import { getWorkflowsIds, putWorkflow } from '../../utils/api';

function workflowExists(id, workflowsIds) {
  return workflowsIds.data.identifiers.includes(id);
}

// DOC: Save to server button with its spinner
export default function SaveToServer({ saveToServerF }) {
  const setGettingFromServer = state((st) => st.setGettingFromServer);
  const setCanvasGraphChanged = state((st) => st.setCanvasGraphChanged);
  const graphRF = state((state) => state.graphRF);
  const workingGraph = state((state) => state.workingGraph);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const [openSaveDialog, setOpenSaveDialog] = useState<boolean>(false);
  const [action, setAction] = useState<string>('newGraph');

  useEffect(() => {
    saveToServerF.current = saveToServer;
  });

  async function saveToServer(): Promise<void> {
    // DOC: Remove empty lines if any in DataMapping, Conditions, DefaultValues
    // and Nodes DataMapping before attempting to save
    let graphRFCurrated = curateGraph(graphRF);
    // DOC: search if id exists.
    // 1. If notExists open dialog for NEW NAME.
    // 2. If exists and you took it from me UPDATE without asking
    // 3. If exists and you took it from elseware open dialog for new name OR OVERWRITE
    const workflowsIds = await getWorkflowsIds();
    setGettingFromServer(true);
    const exists = workflowExists(graphRF.graph.id, workflowsIds);

    if (!exists) {
      setAction('newGraph');
      setOpenSaveDialog(true);
    } else if (workingGraph.graph.id === graphRF.graph.id) {
      if (graphRF.graph.uiProps.source === 'fromServer') {
        // DOC: remove the 'fromServer' before saving as ewoksGraph
        if (graphRFCurrated.graph.uiProps.source) {
          /* eslint-disable @typescript-eslint/no-unused-vars */
          const { source, ...uiPropsNoSource } = graphRFCurrated.graph.uiProps;
          graphRFCurrated = {
            ...graphRFCurrated,
            graph: { ...graphRFCurrated.graph, ...uiPropsNoSource },
          };
        }

        try {
          await putWorkflow(rfToEwoks(graphRFCurrated));
          setOpenSnackbar({
            open: true,
            text: 'Graph saved succesfully!',
            severity: 'success',
          });
          setCanvasGraphChanged(false);
        } catch (error) {
          setOpenSnackbar({
            open: true,
            text: error.response?.data?.message || configData.savingError,
            severity: 'error',
          });
        } finally {
          setGettingFromServer(false);
        }
      } else if (graphRF.graph.uiProps.source !== 'fromServer') {
        setAction('newGraphOrOverwrite');
        setOpenSaveDialog(true);
      } else {
        setGettingFromServer(false);
        setOpenSnackbar({
          open: true,
          text: 'No graph exists to save!',
          severity: 'warning',
        });
      }
    } else {
      setGettingFromServer(false);
      setOpenSnackbar({
        open: true,
        text:
          'Cannot save any changes to subgraphs! Open it as the main graph to make changes.',
        severity: 'warning',
      });
    }
  }

  return (
    <>
      <FormDialog
        elementToEdit={graphRF}
        action={action}
        open={openSaveDialog}
        setOpenSaveDialog={setOpenSaveDialog}
      />
      <IntegratedSpinner
        tooltip="Save to Server"
        action={() => null}
        getting={false}
        onClick={saveToServer}
      >
        <CloudUploadIcon />
      </IntegratedSpinner>
    </>
  );
}
