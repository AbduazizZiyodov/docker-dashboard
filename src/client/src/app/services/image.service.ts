import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Image, ImageSearchResult } from '@models/image';
import { Container } from '@models/container'

@Injectable({
  providedIn: 'root'
})
export class ImageService {

  api: string = 'http://127.0.0.1:2120/api';

  constructor(private http: HttpClient) { }

  all() {
    return this.http.get<Image[]>(`${this.api}/images`);
  }

  get(image_id: string) {
    return this.http.get<Image>(`${this.api}/images/${image_id}`);
  }

  delete(image_id: string) {
    return this.http.delete(`${this.api}/images/${image_id}/remove/`);
  }
  search(term: string, limit: number) {
    return this.http.get<ImageSearchResult[]>(`${this.api}/images/search`, {
      params: {
        term, limit
      }
    });
  }

  containers(image_id: string) {
    return this.http.get<Container[]>(`${this.api}/images/${image_id}/containers`);
  }

}


