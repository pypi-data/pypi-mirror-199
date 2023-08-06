Create and Edit a Workflow
==========================

New Workflow
------------

By clicking the **New** button with the tooltip *start a new workflow* on the upper bar a dialog appears requesting the new workflow **name**. By inserting a unique name and pressing **SAVE WORKFLOW** the dialog disappears and the canvas is available with the name entered appearing in the upper bar left side. If the given name is already used a message warns the user for providing another name.

Open a Workflow
---------------

The user can open a graph in the canvas from:

 - the **server** by searching using the dropdown in the upper bar and pressing the **Open from server**. The workflows management tab can also be used to open-delete a workflow. It is located in the upper drawer that open when pressing the second button from the right in the upper bar. In the workflow management bar a workflow can be selected exploiting the categories dropdown for easier search. Its details are being fetched and presented to the user after selection. Using the 2 buttons under the search boxes the user can open a workflow on the canvas or **delete** it from the server.
 - the **local storage** by pressing the button with the directory icon on the upper bar.


Save a Workflow
---------------

A workflow that is being edited in the canvas can be saved-updated either in the local storage or on the server.
To save a workflow locally tha button with the save icon in the upper bar should be pressed.
To save a workflow on the server the button with the cloud-up-arrow should be pressed. Saving a new workflow on the server involves searching for other workflows with the same name and informing the user.

Edit a Workflow
---------------

On the left sidebar under the Edit Graph dropdown the following can be edited:

 - the **Label** of the graph,
 - the **Comment** that can keep useful user notes about the graph and
 - the **Category** the specific graph belongs. By inserting a category the user can later filter his graphs based on the categories assigned to them making it easier to locate and explore graphs.

**Graph** is made up from **nodes and links** between the nodes. A node can be the representation of a:
 1. **task**
 2. **graph** that can be imported in a graph as a **subgraph**

To **add a node** you need to drag-and-drop one *Task* from the *Add Node* section of the sidebar on the left. The **Add Node** is populated with **Tasks** within their **Categories**.
Tasks are embedded in the system or added by the end-user. Nodes can be seen as an instance of a Task which represents a piece of code. Click for a deeper explanation of the [Ewoks concepts](https://ewokscore.readthedocs.io/en/latest/definitions.html).

A **subgraph** can be added to the graph from the server or from the local storage.

The embedded Tasks are in the category *General* and include: **input**, **output** and **skeleton** tasks.
Input and output are used for declaring the input and the output of a graph respectively.
They can be connected to ONLY ONE node in a given graph.
The task_skeleton is given as an empty cell when the user needs to get a node in the graph without having the
task with which is conected already defined.
In the *General* category 2 more icons represent the icon node that can be added and a *+G* which is used
to add a subgraph from the local storage to the graph.

Adding a subgraph in the graph is done by:
 - using the **+G** from the *sidebar->Add Nodes->General* category for graphs located in our hard-disk
 - using the *down arrow* on the top-bar for graphs that exist on the server.

A *subgraph* is represented in the graph as a node with multiple inputs and outputs. When *doubleclicking* on
a subgraph the canvas shows the subgraph internals i.e. another graph. To get back on the initial graph click
on the topbar left side where a path is created that provides the path to the upper graph.

Nodes can be conected with links that can be created in 2 ways:
 1. by clicking on the handles that the nodes have on their sides and sliding without releasing the click to a handle of another node.
 2. by clicking on a handle and then on another handle.

Every change you make on a graph including the addition og nodes and links can be undone and redone using the
**Undo-Redo** buttons on the top-bar.

Nodes and Links have **node-properties** and **link-properties** respectively that can be further edited on the sidebar.
These properties comply to the `ewoks <https://ewoks.readthedocs.io/>` specification.
A graph can be saved and retrieved from the local-drive or from the server using the buttons on the top-bar.
Every button has a tooltip that appears on hover and describes its functionality.
