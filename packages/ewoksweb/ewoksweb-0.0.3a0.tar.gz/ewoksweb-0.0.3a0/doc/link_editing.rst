Link editing
============

Link editing is hosted on the left-sidebar under the **Edit Node** dropdown when a link on the canvas is selected. If no link is selected the dropdown is:

 - empty if no graph is under editing or
 - depicts the attrubutes of the graph if a graph is under editing and no node or link is selected or
 - depicts the attributes of a node if a node is selected.

Each link has several attributes that follow the `Ewokscore <https://ewokscore.readthedocs.io/en/latest/definitions.html#link-attributes/>`_ specification. On a new link the following items are being depicted:

 - **Label** which is the user-friendly name of a link that appears on the canvas. Above Label there are two buttons that can be used to populate the Label with either the *Conditions* or the *Data Mappings* of the link for the user not to need to type them each time.
 - **Map all Data** where the user can define that no manual data mapping is needed for the links source and target nodes. If unchecked manual Data mapping is revealed.
 - **Data Mapping** where manual data mapping can take place for the link.
 - on_error which is a a special condition where a task raises an exception. Cannot be used in combination with Conditions which disappear if on_error is checked.
 - **Conditions** where the user can define the conditions for the link to be activated and move to the next node.
 - **Advanced** that reveals more attributes when checked.

 The properties that are revealed when Advanced is checked are:

 - **Comment** that allows the user to keep some notes of interest about the specific link.
 - The links Source and Target nodes with their Labes.

Link styling
------------

Links can be styled in the dropdown under Edit Link when a link is selected on the canvas. The link style attributed include:

 - **Link type** which if checked depicts the image associated with the task on the canvas and if not checked removes it.
 - **Arrow Head Type** which if checked depicts the label of the node on the canvas and if not checked removes it.
 - **Animated** which applies a moving animation effect on the selected link.
 - **Color** which adds a surrounding frame and colors it with the selected color.
