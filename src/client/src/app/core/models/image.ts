export interface Image {
  id: string;
  name: string;
  short_id: string;
  labels: object;
  star_count?: number;
  is_official?: boolean;
  description?: string;
  is_pulled?: boolean;

  is_pulling?: boolean;
}
