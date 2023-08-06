Editor basic structure
======================

EwoksWeb is web application where users can visually **view/create/edit** their workflows using the `ewoks <https://ewoks.readthedocs.io/>` abstraction model. It mainly employs a canvas where workflows with their Nodes and Links are being visualized and graphically edited.

On startup ewoksWeb presents a lower drawer open with:

 - a button on the left to open the **tutorial-Graph** which a self descriptive set of graphs demonstrating the tools capabilities.
 - a form in the center to either **login** or sign-in when applicable. This is used on a public installation where multiple users can access the tool. In local installations it can be ignored.
 - a set of dropdowns containing the **user manual** for the tool.

The drawer can be closed on clicking outside of it and can be re-opened any time by clicking on the rightmost button on the upper bar.

The general structure of the EwoksWeb User Interface (UI) includes:

 - The **Canvas** for visualizing and editing graphs.
 - The left **Sidebar** for viewing and editing properties of a graph and its things it is made of: nodes and links.
 - The **upper bar** that hosts buttons for saving, opening and executing graphs.
 - Some **Dialogs** and **Drawers** for managing graphs-tasks-executions and icons.

