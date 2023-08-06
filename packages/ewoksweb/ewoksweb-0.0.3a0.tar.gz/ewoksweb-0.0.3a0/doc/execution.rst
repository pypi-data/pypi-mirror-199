Executing workflows
===================
The concept *execute a workflow* is used when a workflow is being send to the `ewoksServer <https://ewoksserver.readthedocs.io/en/latest/>` for each tasks to be executed.

In order for a workflow to be executed it needs:

 - to be open on the canvas and
 - the button execution from the top-bar menu to be pressed.

The UI enters the execution mode and starts receiving **events** from the ewoksServer that report on the progress of the execution.
According to the events that carry the start and the end of a task execution the UI starts animating the nodes that are being executed updating the workflow graph with numbers that represent the events being received.

The number-events are clickable by the user and on-click the details of each event are being shown in the left-sidebar. In the sidebar all our current executions are being populated and by clicking on each they expand showing some details about the execution. If the **replay** button is pressed the execution as happened with all its events is being drawn on the canvas.

The executions can also be removed as irrelevant from the sidebar by using the **delete** button which is next to the replay button. By clicking on delete the executions remain on the server and can be retrieved at any time by pressing the **All executions** button.

All Executions open a top-drawer in the execution tab where the user can manage the executions that are on the server. A wide list of filters is available to get the executions needed. In the table the user can select one or more executions and by pressing the eye-view that replaces the filters can move the selected executions to the left-sidebar. There the user can inspect and replay the executions he previously selected in the All-executions table.

