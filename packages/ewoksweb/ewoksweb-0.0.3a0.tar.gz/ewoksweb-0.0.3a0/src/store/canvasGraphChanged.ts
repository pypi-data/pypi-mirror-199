const canvasGraphChanged = (set) => ({
  canvasGraphChanged: false,

  setCanvasGraphChanged: (isChanged) => {
    set((state) => ({
      ...state,
      canvasGraphChanged: isChanged,
    }));
  },
});

export default canvasGraphChanged;
