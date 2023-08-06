import Snackbar from '@material-ui/core/Snackbar';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';

import { Alert, Color } from '@material-ui/lab';
import state from '../../store/state';

function SimpleSnackbar() {
  const openSnackbar = state((state) => state.openSnackbar);
  const setOpenSnackbar = state((state) => state.setOpenSnackbar);

  const handleClose = (
    event: React.SyntheticEvent | React.MouseEvent,
    reason?: string
  ) => {
    if (reason === 'clickaway') {
      return;
    }

    setOpenSnackbar({
      open: false,
      text: '',
      severity: 'success',
    });
  };

  const action = (
    <IconButton
      size="small"
      aria-label="close"
      color="inherit"
      onClick={handleClose}
    >
      <CloseIcon fontSize="small" />
    </IconButton>
  );

  return (
    <Snackbar
      open={openSnackbar.open}
      autoHideDuration={6000}
      onClose={handleClose}
      message={openSnackbar.text}
      action={action}
    >
      <Alert onClose={handleClose} severity={openSnackbar.severity as Color}>
        {openSnackbar.text}
      </Alert>
    </Snackbar>
  );
}

export default SimpleSnackbar;
