import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ContainerService } from '@services/container.service';
import { ContainerLogsData } from '@models/container'

@Component({
  selector: 'app-logs-modal',
  template: `
    <div class="text-center" data-aos="flip-up" data-aos-duration="500">
      <h2 class="fw-bold m-1">Logs:{{ container }}</h2>
      <textarea name="" id="" cols="80" rows="10" disabled>
    {{ logs  }}
  </textarea>
    </div>
  `,
})
export class LogsComponent implements OnInit {
  logs!: string;
  container!: string;

  container_id: string = this.route.snapshot.params['id'];
  constructor(
    private containerService: ContainerService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    this.containerService
      .getLogs(this.container_id).subscribe((response: ContainerLogsData) => {
        this.logs = response.logs;
        this.container = response.container;
      });
  }
}
