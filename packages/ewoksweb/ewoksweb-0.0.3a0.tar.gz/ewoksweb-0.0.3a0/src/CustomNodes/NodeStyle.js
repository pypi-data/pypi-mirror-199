export const contentStyle = {
  contentHeader: {
    padding: '8px 0px',
    flexGrow: 1,
    backgroundColor: '#eee',
  },
  io: {
    position: 'relative',
    padding: '8px 16px',
    flexGrow: 1,
    borderRadius: '15px',
  },
  borderInput: {
    border: '1px solid rgb(230, 190, 118)',
  },
  borderOutput: {
    border: '1px solid rgb(118, 133, 221)',
  },
  left: { left: '-8px' },
  textLeft: { textAlign: 'left' },
  right: { right: '-8px' },
  textRight: { textAlign: 'right' },
  handle: {
    zIndex: 1000, // Uncomment
    widht: '20px', // Does not work
    height: '20px',
    margin: 'auto',
    background: '#ddd',
    borderRadius: '15px',
    border: '2px solid rgb(118, 133, 221)',
    boxShadow:
      'rgba(0, 0, 0, 0.2) 0px 1px 3px 0px, rgba(0, 0, 0, 0.14) 0px 1px 1px 0px, rgba(0, 0, 0, 0.12) 0px 2px 1px -1px',
  },
  handleSource: {
    width: '10px',
    border: '2px solid rgb(118, 133, 221)',
  },
  handleTarget: {
    width: '10px',
    border: '2px solid rgb(230, 190, 118)',
  },
  handleUpDown: {
    // height: '18px',
    // background: 'rgb(221, 221, 221)',
    // width: '11px',
  },
};

export const style = {
  icons: {
    maxWidth: '100px',
  },

  body: {
    display: 'flex',
    flexDirection: 'column',
    // backgroundColor: 'rgb(217, 223, 255)',
    transition: 'all 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms',
    boxShadow: '0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23)',
    border: '2px solid #bbb',
    borderRadius: '15px', // TODO: radius to 50 to create a cycle like orange
    fontSize: '10pt',
  },
  selected: {
    boxShadow: '0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)',
  },
  title: {
    position: 'relative',
    padding: '8px 8px',
    flexGrow: 1,
    backgroundColor: '#ee1',
    // zIndex: '-2',
  },
  contentWrapper: {
    padding: '8px 0px',
  },
};
