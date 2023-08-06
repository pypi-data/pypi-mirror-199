const undoIndex = (set, get) => ({
  undoIndex: 0 as number,

  setUndoIndex: (index) => {
    const prevState = get((prev) => prev);

    if (index >= 0 && prevState.undoRedo.length > index) {
      set((state) => ({
        ...state,
        undoIndex: index,
        graphRF: prevState.undoRedo[index].graph,
      }));
      // After setting the new GraphRF the selected element needs
      // to be updated to see the change in the sidebar again on undo-redo
      let selEl = prevState.selectedElement;

      if ('position' in selEl) {
        selEl = prevState.undoRedo[index].graph.nodes.find(
          (nod) => nod.id === selEl.id
        );
        if (selEl) {
          prevState.setSelectedElement(selEl);
        }
      } else if ('source' in selEl) {
        selEl = prevState.undoRedo[index].graph.links.find(
          (lin) => lin.id === selEl.id
        );
        if (selEl) {
          prevState.setSelectedElement(selEl);
        }
      } else if ('output_nodes' in selEl) {
        prevState.setSelectedElement(prevState.undoRedo[index].graph.graph);
      }
    } else {
      prevState.setOpenSnackbar({
        open: true,
        text: 'No more back or forth!',
        severity: 'warning',
      });
    }
  },
});

export default undoIndex;
