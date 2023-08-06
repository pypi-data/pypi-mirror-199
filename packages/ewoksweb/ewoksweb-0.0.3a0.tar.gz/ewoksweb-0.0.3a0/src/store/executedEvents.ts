import type { Event } from '../types';

// DOC: All the events that came in during live executions. These events keep
// pilling-up while the app is up front-back. When should that stop;
const executedEvents = (set, get) => ({
  executedEvents: [] as Event[],

  setExecutedEvents: (execEvent: Event) => {
    // Add all events to keep track of the order they came in
    const prevState = get((prev) => prev);
    // calculate the id of the event based on the order of arrival
    const event = {
      ...execEvent,
      id: prevState.executedEvents.length as number,
    };
    // send it to executing events to adapt the canvas
    prevState.setExecutingEvents(event, true);
    set((state) => ({
      ...state,
      executedEvents: [...prevState.executedEvents, event],
    }));
  },
});

export default executedEvents;
