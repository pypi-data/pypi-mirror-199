import React, { useEffect, useState } from 'react';
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  Button,
  Typography,
} from '@material-ui/core';
import AddNodes from './AddNodes';
import EditElement from './EditElement';
import EditElementStyle from './EditElementStyle';
import DraggableDialog from '../General/DraggableDialog';
import IconMenu from './IconMenu';
import ExecutionDetails from '../Execution/ExecutionDetails';
import DashboardStyle from '../../layout/DashboardStyle';
import state from 'store/state';
import type {
  EwoksRFNode,
  EwoksRFLink,
  GraphDetails,
  GraphRF,
  Icon,
} from 'types';
import { calcNewId } from 'utils/calcNewId';
import ConfirmDialog from 'Components/General/ConfirmDialog';
import { deleteWorkflow, getIcon, getIcons, getOtherIcon } from 'utils/api';
import axios from 'axios';
import path from 'path';
import { OpenInBrowser } from '@material-ui/icons';
import SidebarTooltip from './SidebarTooltip';

const useStyles = DashboardStyle;

export default function Sidebar() {
  const classes = useStyles();

  const selectedElement = state<EwoksRFNode | EwoksRFLink | GraphDetails>(
    (state) => state.selectedElement
  );
  const setSelectedElement = state((state) => state.setSelectedElement);

  const [element, setElement] = useState<
    EwoksRFNode | EwoksRFLink | GraphDetails
  >({});
  const [openExecutionDetails, setOpenExecutionDetails] = useState<boolean>(
    false
  );
  const graphRF = state((state) => state.graphRF);
  const setGraphRF = state((state) => state.setGraphRF);
  const workingGraph = state((state) => state.workingGraph);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const [openDialog] = useState<boolean>(false);
  const [dialogContent] = useState({});
  const setSubgraphsStack = state((state) => state.setSubgraphsStack);
  const setRecentGraphs = state((state) => state.setRecentGraphs);
  const initializedRFGraph = state((state) => state.initializedRFGraph);
  const setUndoRedo = state((state) => state.setUndoRedo);
  const inExecutionMode = state((state) => state.inExecutionMode);
  const [openAgreeDialog, setOpenAgreeDialog] = useState<boolean>(false);
  const setAllIcons = state((state) => state.setAllIcons);
  const allIcons = state((state) => state.allIcons);
  const setAllIconNames = state((state) => state.setAllIconNames);

  useEffect(() => {
    setElement(selectedElement);
  }, [selectedElement]);

  // TODO move fetch out to be used when refresh in icons is needed
  useEffect(
    () => {
      const fetchIcons = async () => {
        if (allIcons.length <= 1) {
          const data = await getIcons();

          const iconsPng = data.identifiers.filter((str) => {
            return !str.endsWith('svg');
          });

          await axios
            .all(iconsPng.map((id: string) => getOtherIcon(id)))
            .then(
              axios.spread((...resPng) => {
                const resCln = resPng.filter((result) => result.data !== null);
                return resCln.map((result) => {
                  const blobPng = new Blob([result.data], {
                    type: 'image/png',
                  });
                  const fileReader = new FileReader();
                  fileReader.readAsDataURL(blobPng);

                  return result.data;
                });
              })
            )
            .catch((error) => {
              // remove after handling the error
              setOpenSnackbar({
                open: true,
                text: error.data,
                severity: 'error',
              });
              return [];
            });

          const iconsSvg = data.identifiers.filter((str) => {
            return str.endsWith('svg');
          });

          setAllIconNames([...iconsSvg, ...iconsPng]);
          const results = await axios
            .all(iconsSvg.map((id: string) => getIcon(id)))
            .then(
              axios.spread((...res) => {
                const resCln = res.filter((result) => result.data !== null);
                return resCln.map((result) => {
                  return {
                    name: path.basename(result.config.url),
                    image: result.data,
                    type: path.extname(result.config.url),
                  };
                });
              })
            )
            .catch((error) => {
              // remove after handling the error
              setOpenSnackbar({
                open: true,
                text: error.data,
                severity: 'warning',
              });
              return [];
            });
          setAllIcons(results as Icon[]);
        }
      };
      // eslint-disable-next-line promise/prefer-await-to-callbacks
      fetchIcons().catch((error) => {
        // Keep logging in console for debugging when talking with a user
        /* eslint-disable no-console */
        console.log(error);
      });
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  const deleteElement = async () => {
    let newGraph = {} as GraphRF;
    const elN = element as EwoksRFNode; // TODO: is this the way to avoid typescript warning???
    const elL = element as EwoksRFLink;
    const elD = element as GraphDetails;
    if (elN.position) {
      const nodesLinks = graphRF.links.filter(
        (link) => !(link.source === elN.id || link.target === elN.id)
      );

      newGraph = {
        ...graphRF,
        nodes: graphRF.nodes.filter((nod) => nod.id !== element.id),
        links: nodesLinks,
      };

      setUndoRedo({
        action: 'Removed a Node',
        graph: newGraph,
      });
    } else if (elL.source) {
      newGraph = {
        ...graphRF,
        links: graphRF.links.filter((link) => link.id !== elL.id),
      };

      setUndoRedo({
        action: 'Removed a Link',
        graph: newGraph,
      });
    }

    if (elD.input_nodes && elD.id !== 'newGraph') {
      setOpenAgreeDialog(true);
    } else if (!elD.input_nodes) {
      if (workingGraph.graph.id === graphRF.graph.id) {
        setGraphRF(newGraph, true);
      } else {
        setOpenSnackbar({
          open: true,
          text: 'Not allowed to delete any element in a sub-graph!',
          severity: 'success',
        });
      }
    } else {
      setOpenSnackbar({
        open: true,
        text: 'Nothing to delete!',
        severity: 'error',
      });
    }
  };

  // TODO: examine if is needed as a feature
  // const showEwoksGraph = () => {
  //   setOpenDialog(true);
  //   setDialogContent({
  //     title: 'Ewoks Graph',
  //     object: rfToEwoks(graphRF),
  //     openFrom: 'sidebar',
  //   });
  // };

  const agreeCallback = async () => {
    setOpenAgreeDialog(false);
    try {
      await deleteWorkflow(element.id);
      setOpenSnackbar({
        open: true,
        text: `Workflow ${element.id} succesfully deleted!`,
        severity: 'success',
      });
    } catch (error) {
      setOpenSnackbar({
        open: true,
        text: error.message,
        severity: 'error',
      });
    }

    setGraphRF(initializedRFGraph);
    setSelectedElement({} as GraphDetails);
    setSubgraphsStack({ id: 'initialiase', label: '' });
    setRecentGraphs({} as GraphRF, true);
  };

  const disAgreeCallback = () => {
    setOpenAgreeDialog(false);
  };

  const cloneNode = () => {
    if ('position' in selectedElement) {
      const newClone = {
        ...selectedElement,
        id: calcNewId(selectedElement.id, graphRF.nodes),
        selected: false,
        position: {
          x: selectedElement.position.x + 100,
          y: selectedElement.position.y + 100,
        },
      };
      const newGraph = {
        ...graphRF,
        nodes: [...graphRF.nodes, newClone],
      };

      setGraphRF(newGraph, true);

      setUndoRedo({ action: 'Cloned a Node', graph: newGraph });
      setSelectedElement(newClone as EwoksRFNode);
    } else {
      setOpenSnackbar({
        open: true,
        text: 'Clone is for cloning nodes within the working workflow',
        severity: 'warning',
      });
    }
  };

  const handleChangeExecutionDetails = (
    event: React.SyntheticEvent,
    expand: boolean
  ) => {
    setOpenExecutionDetails(expand);
  };

  return (
    <aside className="dndflow">
      {!inExecutionMode && (
        <>
          <AddNodes title="Add Nodes" />
          <EditElement element={selectedElement} />
          <EditElementStyle />
        </>
      )}
      <Accordion
        expanded={openExecutionDetails}
        onChange={handleChangeExecutionDetails}
        className="Accordions-sidebar"
      >
        <AccordionSummary
          expandIcon={<OpenInBrowser />}
          aria-controls="panel1a-content"
          className="Accordions-sidebar"
        >
          <SidebarTooltip
            text={`Drag and drop Tasks from their categories
          to the canvas to create graphs.`}
          >
            <Typography>Execution History</Typography>
          </SidebarTooltip>
        </AccordionSummary>
        <AccordionDetails style={{ flexWrap: 'wrap', padding: '4px' }}>
          <div className={classes.executionSide}>
            <ExecutionDetails />
          </div>
        </AccordionDetails>
      </Accordion>
      {!inExecutionMode && (
        <>
          <Button
            style={{ margin: '8px' }}
            variant="outlined"
            color="secondary"
            onClick={deleteElement}
            size="small"
          >
            Delete
          </Button>
          <Button
            style={{ margin: '8px' }}
            variant="outlined"
            color="primary"
            onClick={cloneNode}
            size="small"
            data-cy="cloneButton"
          >
            Clone
          </Button>
          {!('source' in selectedElement) && <IconMenu />}
          <DraggableDialog open={openDialog} content={dialogContent} />
          <ConfirmDialog
            title={`Delete "${element.label}" workflow?`}
            content={`You are about to delete "${element.label}" workflow.
              Please make sure that it is not used as a subgraph in other workflows!
              Do you agree to continue?`}
            open={openAgreeDialog}
            agreeCallback={agreeCallback}
            disagreeCallback={disAgreeCallback}
          />
        </>
      )}
    </aside>
  );
}
