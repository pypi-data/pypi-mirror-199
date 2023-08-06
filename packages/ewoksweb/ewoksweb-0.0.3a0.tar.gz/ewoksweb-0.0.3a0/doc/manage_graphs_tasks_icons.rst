Managing EwoksWeb Entities
==========================
By pressing the second button from the right in the upper bar the managing upper drawer reveals itself. In different tabs the user can manage: workflows, tasks, icons and executions.

Managing Workflows
------------------

The workflows management tab can be used to open, inspect and delete a workflow. In the workflow management bar a workflow can be selected exploiting the categories dropdown for easier search. Its details are being fetched and presented to the user after selection. Using the 2 buttons under the search boxes the user can open a workflow on the canvas or **delete** it from the server.

Managing Tasks
--------------

Tasks can be managed in the second tab of the upper drawer. By clicking on the dropdown the tasks in their categories are revealed with their assigned icons. When clicking on a task underneath it buttons appear for deleting, editing and cloning the task. By deleting the task it is removed from the server permanently and can affect the workflows that contain it if any.
Editing and cloning opens a dialog with all task properties below also described in `Ewokscore <https://ewokscore.readthedocs.io/en/latest/definitions.html#task-implementation/>`_:

 - New Name - Identifier: the Task will be saved to file with this name-identifier.
 - Task Type
 - Category
 - Optional Inputs
 - Required Inputs
 - Outputs
 - Icon which is the icon that will appear in the task and in the nodes that will be created from this task.

Tasks can be discovered in the server if the slider **Task Discovery** is used. When is set it open an input where the module name will be inserted and a button to start the discovery process on the server. The process assumes that the absolute path to the python module is given for the discovery mechanism to find the python tasks described in there.

Managing Icons
--------------

Icons can be added and removed from the system. An icon can be any small image (under development)

Managing Executions
-------------------

For execution management refer to `Executing Workflows <https://ewoksweb.readthedocs.io/en/latest/execution.html#executing-workflows/>`_ section.

