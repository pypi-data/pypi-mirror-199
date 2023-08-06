import React, { useEffect } from 'react';
import { Button } from '@material-ui/core';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';

interface ConfirmDialogProps {
  open: boolean;
  title: string;
  content: string;
  agreeCallback(isSubgraph?: string): Promise<void> | void;
  disagreeCallback(): void;
}
// DOC: Used as an app-wide dialog when confirmation is needed. Open is a prop
export default function ConfirmDialog(props: ConfirmDialogProps) {
  const { open, title, content } = props;

  const [isOpen, setIsOpen] = React.useState(false);

  useEffect(() => {
    setIsOpen(open);
  }, [open]);

  const handleDisagree = () => {
    setIsOpen(false);
    props.disagreeCallback();
  };

  const handleAgree = () => {
    setIsOpen(false);
    props.agreeCallback();
  };

  const handleClose = () => {
    setIsOpen(false);
  };

  return (
    <Dialog
      open={isOpen}
      onClose={handleClose}
      aria-labelledby="alert-dialog-title"
      aria-describedby="alert-dialog-description"
    >
      <DialogTitle id="alert-dialog-title">{title}</DialogTitle>
      <DialogContent>
        <DialogContentText id="alert-dialog-description">
          {content}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={handleDisagree}>No</Button>
        <Button onClick={handleAgree}>Yes</Button>
      </DialogActions>
    </Dialog>
  );
}
