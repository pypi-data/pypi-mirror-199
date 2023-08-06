import Popover from '@material-ui/core/Popover';
import SaveGetFromDisk from '../TopNavBar/SaveGetFromDisk';

interface MenuPopoverProps {
  anchorEl: null | HTMLElement;
  handleClose(): void;
}
export default function MenuPopover({
  anchorEl,
  handleClose,
}: MenuPopoverProps) {
  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  return (
    <div>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'center',
        }}
        transformOrigin={{
          vertical: 'top',
          horizontal: 'center',
        }}
      >
        <SaveGetFromDisk />
      </Popover>
    </div>
  );
}
