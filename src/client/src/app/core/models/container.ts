import { Image } from './image';

export interface Container {
  id: string;
  name: string;
  status: string | any;
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