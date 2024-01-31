import { Image } from './image'

export enum ContainerStatus {
  dead = "dead",
  exited = "exited",
  paused = "paused",
  running = "running",
  created = "created",
  restarting = "restarting"
}

export interface Container {
  id: string;
  name: string;
  status: ContainerStatus;
  short_id: string;
  labels: object;
  image: Image;
}

export interface RunContainerData {
  name?: string;
  image?: string;
  command?: string;
  entrypoint?: string;
  ports?: object;
  firstPort?: string;
  secondPort?: string;
}


export interface ContainerLogsData {
  logs: string;
  container: string;
}

export interface ContainerActionStatusResponse {
  container_id: string
  status: ContainerStatus
}