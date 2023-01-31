import { Component, OnInit } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

import { environment } from '@env';
import { Task } from '@models/image';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-pull-list',
  templateUrl: './pull-list.component.html',
})
export class PullListComponent implements OnInit {
  tasks!: Task[];
  ws!: WebSocketSubject<any>;
  sockets: WebSocketSubject<any>[] = [];
  multiplePullingEnabled: boolean = false;

  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
    this.ws = webSocket(`${environment.wsUrl}/images/pull`);

    this.ws.next({ action: 'list' });
    this.ws.asObservable().subscribe((data: any) => {
      this.tasks = data;
    });
  }
  start(repository: string, tag: string): void {
    this.toastr.warning('Creating & connecting websocket ...');
    let ws = this.multiplePullingEnabled ? this.createNewSocket() : this.ws;
    ws.next({ repository, tag, action: 'start' });
    ws.asObservable().subscribe((data: any) => {
      this.tasks = data;
    });
  }

  delete(repository: string, tag: string): void {
    this.ws.next({ repository, tag, action: 'delete' });
    this.ws.asObservable().subscribe((data: any) => {
      this.tasks = data;
    });
  }

  createNewSocket(): WebSocketSubject<any> {
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
}
