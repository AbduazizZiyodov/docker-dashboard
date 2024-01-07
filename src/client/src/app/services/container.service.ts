import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Container } from '@models/container';

@Injectable({
  providedIn: 'root',
})
export class ContainerService {
  api: string = 'http://127.0.0.1:2121/api';
  
  constructor(private http: HttpClient) { }

  all() {
    return this.http.get<Container[]>(`${this.api}/containers`);
  }

  get(container_id: string) {
    return this.http.get<Container>(`${this.api}/containers/${container_id}`);
  }

  // startStoppedContainer(container_id: string) {
  //   return this.http.get(`${this.api}/containers/${container_id}/start`);
  // }

  // stopContainer(container_id: string) {
  //   return this.http.get(`${this.api}/containers/${container_id}/stop`);
  // }

  // deleteContainer(container_id: string) {
  //   return this.http.delete(`${this.api}/containers/${container_id}/delete`);
  // }

  // runContainer(containerData: RunContainerData) {
  //   return this.http.post<Container>(
  //     `${this.api}/containers/run`,
  //     containerData
  //   );
  // }

  // getLogs(container_id: string | undefined) {
  //   return this.http.get<ContainerLogsData>(`${this.api}/containers/${container_id}/logs`);
  // }
}