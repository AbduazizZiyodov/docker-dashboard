import { Component, OnInit } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';

import { environment } from '@env';
import { Task } from '@models/image';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-pull-list',
  templateUrl: './pull-list.component.html',
  styleUrls: ['./pull-list.component.scss'],
})
export class PullListComponent implements OnInit {
  tasks!: Task[];
  ws!: WebSocketSubject<any>;
  sockets: WebSocketSubject<any>[] = [];
  multiplePullingEnabled: boolean = false;

  constructor(private toastr: ToastrService) {}

  ngOnInit(): void {
    this.ws = webSocket(`${environment.wsUrl}/images/pull`);

    this.ws.next({ repository: '', action: 'all' });
    this.ws.asObservable().subscribe((data: any) => {
      this.tasks = data;
    });
  }
  start(repository: string, tag: string): void {
    this.toastr.warning("Creating & connecting websocket ...")
    let ws = this.multiplePullingEnabled ? this.createNewSocket() : this.ws;
    ws.next({ repository: repository, tag: tag, action: 'start' });
    ws.asObservable().subscribe((data: any) => {
      this.tasks = data;
    });

  }

  delete(repository: string, tag: string) {
    this.ws.next({ repository: repository, tag: tag, action: 'delete' });
    this.ws.asObservable().subscribe((data: any) => {
      this.tasks = data;
    });
  }

  ngOnDestroy() {
    this.ws.complete();
    this.sockets.forEach((socket: WebSocketSubject<any>) => {
      socket.complete();
    });
  }

  createNewSocket() {
    let socket = webSocket(`${environment.wsUrl}/images/pull`);
    this.sockets.push(socket);
    return socket;
  }
}
