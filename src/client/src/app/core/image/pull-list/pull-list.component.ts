import { Component, OnInit } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

import { environment } from '@env';
import { ToastrService } from 'ngx-toastr';

type Data = {
  tag: string;
  status: string;
  repository: string;
  stream_data: string;
};

@Component({
  selector: 'app-pull-list',
  templateUrl: './pull-list.component.html',
})
export class PullListComponent implements OnInit {
  tasks: { [key: string]: Data } = {};
  sockets: WebSocketSubject<any>[] = [];
  multiplePullingEnabled: boolean = false;
  ws: WebSocketSubject<any> = webSocket(`${environment.wsUrl}/images/pull`);

  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
    this.fetchRepositories();
  }

  fetchRepositories(): void {
    this.ws.next({ repository: '', action: 'list' });

    this.ws.asObservable().subscribe((data: any) => {
      this.createTasks(data);
    });
  }

  createTasks(images: string[]): void {
    for (let task of images) {
      const [repository, tag] = this.splitRepositoryAndTag(task);

      this.tasks[task] = {
        stream_data: '',
        status: '',
        tag: tag,
        repository: repository,
      };
    }
  }

  start(repository: string, tag: string): void {
    this.toastr.warning('Creating & connecting websocket ...');
    let full_repository_name = `${repository}:${tag}`;

    let ws = this.multiplePullingEnabled ? this.createWebSocket() : this.ws;

    ws.next({ repository, tag, action: 'start' });

    ws.asObservable().subscribe((data: any) => {
      this.tasks[full_repository_name].status = data.status;
      if (data.progress.length) {
        this.tasks[full_repository_name].stream_data = this.tasks[
          full_repository_name
        ].stream_data
          .concat('\n')
          .concat(`[${data.id}] -> ${data.progress}`);
      }
    });
  }

  delete(repository: string, tag: string): void {
    let full_repository_name = `${repository}:${tag}`;

    this.ws.next({ repository, tag, action: 'delete' });
    this.ws.asObservable().subscribe((data: string[]) => {
      delete this.tasks[full_repository_name];
    });
  }

  createWebSocket(): WebSocketSubject<any> {
    let socket = webSocket(`${environment.wsUrl}/images/pull`);
    this.sockets.push(socket);
    return socket;
  }

  ngOnDestroy(): void {
    this.sockets.forEach((socket: WebSocketSubject<any>) => {
      socket.complete();
    });
    this.ws.complete();
  }

  splitRepositoryAndTag(full_repository_name: string): string[] {
    return full_repository_name.split(':');
  }
  numberOfTasks(): number {
    return Object.keys(this.tasks).length;
  }

  getTaskKeys(): string[] {
    return Object.keys(this.tasks);
  }
}
