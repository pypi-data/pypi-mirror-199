import axios, { AxiosResponse } from 'axios';
import type { GraphEwoks, Task, IconsNames } from '../types';

export const axiosRequest = axios.create({
  baseURL: process.env.REACT_APP_SERVER_URL,
});

// --------------Tasks
// Get '/tasks/descriptions'
export function getTaskDescription() {
  return axiosRequest.get(`/tasks/descriptions`);
}

// Delete task
export function deleteTask(id: string) {
  return axiosRequest.delete(`/task/${id}`);
}

// Post task
export function postTask(task: Task) {
  return axiosRequest.post(`/tasks`, task);
}

// Put task
export function putTask(task: Task) {
  return axiosRequest.put(`/task/${task.task_identifier}`, task);
}

// Discover tasks
export function discoverTasks(moduleNames: string[]) {
  return axiosRequest.post(`/tasks/discover`, { modules: moduleNames });
}

// -------------Workflows
// Get /workflows
export function getWorkflowsDescriptions() {
  return axiosRequest.get(`/workflows/descriptions`);
}

// Get /workflows only id
export function getWorkflowsIds() {
  return axiosRequest.get(`/workflows`);
}

// Get workflow:id
export function getWorkflow(id: string) {
  return axiosRequest.get(`/workflow/${id}`);
}

// Post
export function postWorkflow(workflow: GraphEwoks) {
  return axiosRequest.post(`/workflows`, workflow);
}

// Post execute
export function executeWorkflow(workflowId: string) {
  return axiosRequest.post(`/execute/${workflowId}`, workflowId);
}

// Put
export function putWorkflow(workflow: GraphEwoks) {
  return axiosRequest.put(`/workflow/${workflow.graph.id}`, workflow);
}

// Delete
export function deleteWorkflow(id: string) {
  return axiosRequest.delete(`/workflow/${id}`);
}

// Get executed workflows
export function getExecutionEvents(queryParams) {
  const queryString = Object.keys(queryParams)
    .map((key) => `${key}=${queryParams[key] as string}`)
    .join('&');
  return axiosRequest.get(`/execution/events?${queryString}`);
}

// --------------Icons
// Get '/icons/descriptions'
export async function getIcons(): Promise<IconsNames> {
  const result: AxiosResponse<IconsNames> = await axiosRequest.get(`/icons`);
  return result.data;
}

// Get icon:id
export function getIcon(id: string): Promise<AxiosResponse<string>> {
  return axiosRequest.get<string>(`/icon/${id}`);
}

export function getOtherIcon(id: string): Promise<AxiosResponse<string>> {
  return axiosRequest.get(`${process.env.REACT_APP_SERVER_URL}/icon/${id}`, {
    responseType: 'blob',
  });
}
