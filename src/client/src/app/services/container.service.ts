import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Container, ContainerLogsData, RunContainerData, ContainerActionStatusResponse } from '@models/container';

@Injectable({
  providedIn: 'root',
})
export class ContainerService {
  api: string = 'http://127.0.0.1:2120/api';

  constructor(private http: HttpClient) { }

  all() {
    return this.http.get<Container[]>(`${this.api}/containers`);
  }

  get(container_id: string) {
    return this.http.get<Container>(`${this.api}/containers/${container_id}`);
  }

  start(container_id: string) {
    return this.http.get<ContainerActionStatusResponse>(`${this.api}/containers/${container_id}/start`);
  }

  stop(container_id: string) {
    return this.http.get<ContainerActionStatusResponse>(`${this.api}/containers/${container_id}/stop`);
  }

  pause(container_id: string) {
    return this.http.get<ContainerActionStatusResponse>(`${this.api}/containers/${container_id}/pause`);
  }
  delete(container_id: string) {
    return this.http.delete(`${this.api}/containers/${container_id}/delete`);
  }

  run(containerData: RunContainerData) {
    return this.http.post<Container>(
      `${this.api}/containers/run`,
      containerData
    );
  }

  kill(containerId: string, signal?: string) {
    if (signal == undefined) { signal = 'SIGKILL' }
    return this.http.get<ContainerActionStatusResponse>(`${this.api}/containers/${containerId}/kill?signal=${signal}`)
  }

  logs(container_id: string | undefined) {
    return this.http.get<ContainerLogsData>(`${this.api}/containers/${container_id}/logs`);
  }

}