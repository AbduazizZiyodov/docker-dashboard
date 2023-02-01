import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ContainerService } from '@services/container.service';
import { map, Observable } from 'rxjs';

@Component({
  selector: 'app-logs-modal',
  template: `
    <div class="text-center" data-aos="flip-up" data-aos-duration="500">
      <h1 class="fw-bold m-1">Logs</h1>
      <textarea name="" id="" cols="80" rows="10" disabled>
    {{ logs$ | async }}
  </textarea>
    </div>
  `,
})
export class LogsComponent implements OnInit {
  logs$ = new Observable<string>();
  container_id: string = this.route.snapshot.params['id'];
  constructor(
    private containerService: ContainerService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.logs$ = this.containerService
      .getLogs(this.container_id)
      .pipe(map((response: any) => response['logs']));
  }
}
