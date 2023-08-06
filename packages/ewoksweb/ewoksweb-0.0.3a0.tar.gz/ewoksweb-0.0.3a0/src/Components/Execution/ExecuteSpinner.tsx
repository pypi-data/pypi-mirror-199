/* eslint-disable react/no-unused-prop-types */
import React, { ReactNode } from 'react';
import Box from '@material-ui/core/Box';
import CircularProgress from '@material-ui/core/CircularProgress';
import Fab from '@material-ui/core/Fab';
import CheckIcon from '@material-ui/icons/Check';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
  top: {
    animationDuration: '550ms',
    position: 'absolute',
    left: 60,
  },
  openFileButton: {
    width: '62px',
    height: '62px',
  },
}));

interface ExecuteSpinnerProps {
  getting: boolean;
  children: ReactNode;
  tooltip?: string;
  action?(): void;
}

export default function ExecuteSpinner(props: ExecuteSpinnerProps) {
  const [loading, setLoading] = React.useState(false);
  const [success] = React.useState(false);
  const classes = useStyles();

  // TODO: synd with the real time the call makes using getting
  React.useEffect(() => {
    if (props.getting) {
      setLoading(true);
    } else {
      setLoading(false);
    }
  }, [props.getting]);

  return (
    <Box sx={{ display: 'flex', alignItems: 'center' }}>
      <Box sx={{ m: 1, position: 'relative' }}>
        <Fab
          className={classes.openFileButton}
          size="large"
          component="span"
          aria-label="add"
        >
          {success ? <CheckIcon /> : loading ? '...' : props.children}
        </Fab>
        {loading && (
          <CircularProgress
            size={66}
            className={classes.top}
            thickness={4}
            value={100}
            style={{
              color: 'white',
              position: 'absolute',
              top: -3,
              left: -3,
              zIndex: 1,
            }}
          />
        )}
      </Box>
    </Box>
  );
}
