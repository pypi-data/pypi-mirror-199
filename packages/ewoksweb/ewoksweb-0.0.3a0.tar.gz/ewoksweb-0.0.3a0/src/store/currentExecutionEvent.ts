// DOC: the number of the event we need to inspect on the sidebar
const currentExecutionEvent = (set) => ({
  currentExecutionEvent: 0,

  setCurrentExecutionEvent: (indexOfEvent) => {
    set((state) => ({
      ...state,
      currentExecutionEvent: indexOfEvent,
    }));
  },
});

export default currentExecutionEvent;
