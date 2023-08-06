import DashboardStyle from '../../layout/DashboardStyle';
import Tooltip from '@material-ui/core/Tooltip';
import { Fab, IconButton } from '@material-ui/core';
import SaveIcon from '@material-ui/icons/Save';
import FolderOpenIcon from '@material-ui/icons/FolderOpen';
import Upload from '../General/Upload';
import tooltipText from '../General/TooltipText';
import { rfToEwoks } from '../../utils';

import state from '../../store/state';

const useStyles = DashboardStyle;

function download(content, fileName, contentType) {
  const a = document.createElement('a');
  const file = new Blob([content], { type: contentType });
  a.href = URL.createObjectURL(file);
  a.download = fileName;
  a.click();
}

export default function SaveGetFromDisk() {
  const classes = useStyles();

  const setGraphOrSubgraph = state((state) => state.setGraphOrSubgraph);
  const graphRF = state((state) => state.graphRF);
  const inExecutionMode = state((state) => state.inExecutionMode);

  function loadFromDisk() {
    setGraphOrSubgraph(true);
  }

  function saveToDisk() {
    download(
      JSON.stringify(rfToEwoks(graphRF), null, 2),
      `${graphRF.graph.label}.json`,
      'text/plain'
    );
  }

  return (
    <>
      <Tooltip title={tooltipText('Save to local disk')} enterDelay={800} arrow>
        <span>
          <IconButton color="inherit" onClick={saveToDisk}>
            <Fab
              className={classes.openFileButton}
              color="primary"
              size="small"
              component="span"
              aria-label="add"
            >
              <SaveIcon />
            </Fab>
          </IconButton>
        </span>
      </Tooltip>
      <Tooltip
        title={tooltipText('Load from local disk')}
        enterDelay={800}
        arrow
      >
        <span>
          <IconButton
            color="inherit"
            disabled={inExecutionMode}
            onClick={loadFromDisk}
          >
            <Upload>
              <FolderOpenIcon />
            </Upload>
          </IconButton>
        </span>
      </Tooltip>
    </>
  );
}
