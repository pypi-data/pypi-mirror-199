import React, { useEffect } from 'react';
import Box from '@material-ui/core/Box';
import Drawer from '@material-ui/core/Drawer';
import Divider from '@material-ui/core/Divider';
import BasicTabs from '../TopDrawer/BasicTabs';
import EwoksUiInfo from '../Frontpage/EwoksUiInfo';

type Anchor = 'top' | 'left' | 'bottom' | 'right';

// TODO: to decide if only top is needed and local state of the drawer
export default function SettingsInfoDrawer(props) {
  const [drawerPositions, setDrawerPositions] = React.useState({
    top: false,
    left: false,
    bottom: false,
    right: false,
  });

  useEffect(() => {
    setDrawerPositions({
      top: props.openDrawers && props.openSettings,
      left: false,
      bottom: props.openDrawers && props.openInfo,
      right: false,
    });
  }, [props.openSettings, props.openInfo, props.openDrawers]);

  const toggleDrawer = (anchor: Anchor, open: boolean) => (
    event: React.KeyboardEvent | React.MouseEvent
  ) => {
    if (
      event &&
      event.type === 'keydown' &&
      ((event as React.KeyboardEvent).key === 'Tab' ||
        (event as React.KeyboardEvent).key === 'Shift')
    ) {
      return;
    }
    props.handleOpenDrawers();
    setDrawerPositions({ ...drawerPositions, [anchor]: open }); // left: open , for opening both-active 1
  };

  const list = (anchor: Anchor) => (
    <Box
      sx={{ width: anchor === 'top' || anchor === 'bottom' ? 'auto' : 350 }}
      role="presentation"
    >
      {props.openInfo ? (
        <div className="infoAccordion">
          <EwoksUiInfo closeDialog={toggleDrawer('bottom', false)} />
        </div>
      ) : (
        <BasicTabs />
      )}
      <Divider />
    </Box>
  );

  return (
    <div>
      {(['left', 'top', 'right', 'bottom'] as const).map((anchor) => (
        <React.Fragment key={anchor}>
          {/* <Button onClick={toggleDrawer(anchor, true)}>{anchor}</Button> */}
          <Drawer
            style={{ alignItems: 'center', display: 'flex' }}
            anchor={anchor}
            open={drawerPositions[anchor]}
            onClose={toggleDrawer(anchor, false)}
          >
            {list(anchor)}
          </Drawer>
        </React.Fragment>
      ))}
    </div>
  );
}
