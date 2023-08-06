/* eslint-disable jsx-a11y/control-has-associated-label */
import { makeStyles, createStyles } from '@material-ui/core/styles';
import { Fab } from '@material-ui/core';

// import { validateEwoksGraph } from '../utils/EwoksValidator';
import state from '../../store/state';
import type { GraphRF } from '../../types';

const useStyles = makeStyles(() =>
  createStyles({
    openFileButton: {
      backgroundColor: '#96a5f9',
    },
  })
);

const showFile = async (e): Promise<FileReader> => {
  e.preventDefault();
  const reader: FileReader = new FileReader();
  reader.readAsText(e.target.files[0]);
  return reader;
};

function isJsonString(str: string): boolean {
  try {
    JSON.parse(str);
  } catch (error) {
    /* eslint no-console: ["error", { allow: ["warn", "error"] }] */
    console.warn(error);
    return false;
  }
  return true;
}

function Upload(props) {
  const classes = useStyles();

  const graphRF = state<GraphRF>((state) => state.graphRF);
  const graphOrSubgraph = state<Boolean>((state) => state.graphOrSubgraph);

  const workingGraph = state<GraphRF>((state) => state.workingGraph);
  const setWorkingGraph = state((state) => state.setWorkingGraph);
  const setSubGraph = state((state) => state.setSubGraph);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);
  const inExecutionMode = state<boolean>((state) => state.inExecutionMode);

  async function fileNameChanged(event) {
    if (workingGraph.graph.id === graphRF.graph.id) {
      const reader = showFile(event);
      const file = await reader.then((val) => val);
      // eslint-disable-next-line require-atomic-updates
      file.onloadend = async () => {
        if (isJsonString(file.result as string)) {
          const newGraph = JSON.parse(file.result as string);

          if (graphOrSubgraph) {
            // TODO validate from disk workflows but visualize them
            // const { result } = validateEwoksGraph(newGraph);
            // if (result) {
            await setWorkingGraph(newGraph, 'fromDisk');
            // }
          } else {
            await setSubGraph(newGraph);
          }
        } else {
          setOpenSnackbar({
            open: true,
            text:
              'Error in JSON structure. Please correct input file and retry!',
            severity: 'error',
          });
        }
      };
    } else {
      setOpenSnackbar({
        open: true,
        text: 'Not allowed to add a new node-graph to any sub-graph!',
        severity: 'success',
      });
    }
  }

  return (
    <div>
      <label htmlFor="load-graph">
        <input
          style={{ display: 'none' }}
          id="load-graph"
          name="load-graph"
          type="file"
          onChange={fileNameChanged}
        />
        <Fab
          className={classes.openFileButton}
          color="primary"
          size="small"
          component="span"
          aria-label="add"
          disabled={inExecutionMode}
        >
          {props.children}
        </Fab>
      </label>
    </div>
  );
}

export default Upload;
