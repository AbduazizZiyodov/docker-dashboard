import { Image } from './image';

export interface Container {
  id: string;
  name: string;
  status: string | any;
  short_id: string;
  labels: object;
  image: Image;
}
