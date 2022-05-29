import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Image } from '../models/image';
import { Container } from '../models/container';

@Injectable({
  providedIn: 'root',
})
export class ImageService {
  api: string = environment.apiUrl;
  constructor(private http: HttpClient) {}

  getImages() {
    return this.http.get<Image[]>(`${this.api}/images`);
  }

  deleteImage(image_id: string) {
    return this.http.delete(`${this.api}/images/${image_id}/delete`);
  }

  getContainersByImage(image_id: string) {
    return this.http.get<Image[]>(`${this.api}/images/${image_id}/containers`);
  }
}
