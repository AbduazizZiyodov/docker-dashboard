import { Image } from './image';

export interface Container {
  id: string;
  name: string;
  status: string;
  short_id: string;
  labels: object;
  image: Image;
}
