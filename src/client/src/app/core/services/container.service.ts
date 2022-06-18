import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { Container, RunContainerData } from '@models/container';

@Injectable({
  providedIn: 'root',
})
export class ContainerService {
  api: string = environment.apiUrl;
  constructor(private http: HttpClient) {}

  getContainers() {
    return this.http.get<Container[]>(`${this.api}/containers`);
  }

  getContainer(container_id: string) {
    return this.http.get<Container>(`${this.api}/containers/${container_id}`);
  }

  startStoppedContainer(container_id: string) {
    return this.http.get(`${this.api}/containers/${container_id}/start`);
  }

  stopContainer(container_id: string) {
    return this.http.get(`${this.api}/containers/${container_id}/stop`);
  }

  deleteContainer(container_id: string) {
    return this.http.delete(`${this.api}/containers/${container_id}/delete`);
  }

  runContainer(containerData: RunContainerData) {
    return this.http.post<Container>(
      `${this.api}/containers/run`,
      containerData
    );
  }
}
