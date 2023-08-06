import { useState, useEffect, useRef } from 'react';
import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';
import Fab from '@material-ui/core/Fab';
import CheckIcon from '@material-ui/icons/Check';
import { makeStyles } from '@material-ui/core/styles';
import Tooltip from '@material-ui/core/Tooltip';
import tooltipText from './TooltipText';

import state from '../../store/state';

interface IntegratedSpinnerProps {
  children;
  tooltip: string;
  getting: boolean;
  action(isSubgraph?: string): void;
  onClick?(): void;
}

// DOC: create the round spin effect changing from loading state
// to success and then to the wait state using the image passed as children.
export default function IntegratedSpinner(props: IntegratedSpinnerProps) {
  const { children, tooltip, getting } = props;

  const undoIndex = state((state) => state.undoIndex);

  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  const inExecutionMode = state((state) => state.inExecutionMode);
  const canvasGraphChanged = state((state) => state.canvasGraphChanged);

  const timer = useRef<number>();

  const useStyles = makeStyles(() => ({
    top: {
      animationDuration: '550ms',
      position: 'absolute',
      left: 0,
    },
    openFileButton: {
      backgroundColor:
        tooltip === 'Save to Server' && canvasGraphChanged && undoIndex !== 0
          ? 'red'
          : '#96a5f9',
    },
  }));
  const classes = useStyles();

  // TODO: synd with the real time the call makes using getting
  useEffect(() => {
    if (getting) {
      timer.current = window.setTimeout(() => {
        setLoading(false);
      }, 2000);
    }

    // DOC: clearing the timeout breaks the wanted effect of the tick
    // return () => {
    //   clearTimeout(timer.current);
    // };
  }, [getting]);

  function handleButtonClick() {
    if (!loading) {
      props.onClick();

      if (props.action) {
        props.action();
      }
      setSuccess(false);
      setLoading(true);
      timer.current = window.setTimeout(() => {
        setSuccess(true);
        setLoading(false);
      }, 1500);
      timer.current = window.setTimeout(() => {
        setSuccess(false);
        setLoading(false);
      }, 3000);
    }
  }

  return (
    <Tooltip title={tooltipText(tooltip) || ''} enterDelay={800} arrow>
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <Box sx={{ m: 1, position: 'relative' }}>
          <Fab
            className={classes.openFileButton}
            color="primary"
            size="small"
            onClick={handleButtonClick}
            component="span"
            aria-label="add"
            disabled={
              loading
                ? true
                : tooltip === 'Execute Workflow and exit Execution mode'
                ? false
                : inExecutionMode
            }
          >
            {success ? <CheckIcon /> : loading ? '...' : children}
          </Fab>
          {loading && (
            <CircularProgress
              size={46}
              className={classes.top}
              thickness={4}
              // {...props}
              value={100}
              style={{
                color: 'white',
                position: 'absolute',
                top: -4,
                left: -4,
                zIndex: 1,
              }}
            />
          )}
        </Box>
      </Box>
    </Tooltip>
  );
}
