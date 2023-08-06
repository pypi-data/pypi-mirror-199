const gettingFromServer = (set) => ({
  gettingFromServer: false,

  setGettingFromServer: (val: boolean) => {
    set((state) => ({
      ...state,
      gettingFromServer: val,
    }));
  },
});

export default gettingFromServer;
