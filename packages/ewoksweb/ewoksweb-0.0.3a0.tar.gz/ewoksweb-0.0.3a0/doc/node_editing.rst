Node editing
============

Node editing is hosted on the left-sidebar under the **Edit Node** dropdown when a node on the canvas is selected. If no node is selected the dropdown is:

 - empty if no graph is under editing or
 - depicts the attrubutes of the graph if a graph is under editing and no node or link is selected or
 - depicts the attributes of a link if a link is selected.

Each node has several attributes that follow the  `ewokscore <https://ewokscore.readthedocs.io/en/latest/definitions.html#node-attributes>`_specification. On a new node three items are being depicted:

 - **Label** which is the user-friendly name of a node that the user can always change. Label will initially take the name of the task the specific node is referred to.
 - **Default Inputs** where the user can define inputs for any given node representing a task or a subgraph.
 - **Advanced** that reveals more attributes when checked.

 The properties that are revealed when Advanced is checked are:

 - **Comment** that allows the user to keep some notes of interest.
 - **Inputs-complete** when the default input covers all required input.
 - **Default Error Node** that makes the node to be the default-error-node. Each graph can have zero to one such nodes.
 - **Node Info** which holds read-only information about the selected node.

 When **Default Error Node** is checked the **Map all Data** appears already ticked which means that no extra Data Mapping is needed for the Default Error Node. If unchecked the Map all Data reveals the **Data Mapping** where manual mapping can take place.

Node styling
------------

Nodes can be styled in the dropdown under Edit Node when a node is selected on the canvas. The node style attributed include:

 - **With Image** which if checked depicts the image associated with the task on the canvas and if not checked removes it.
 - **With Label** which if checked depicts the label of the node on the canvas and if not checked removes it.
 - **Color** which adds a surrounding frame and colors it with the selected color.
 - **More handles** which provides additional handles to the node on the top and on the bottom.
 - **Node Size** slider which modifies the size of the node.
