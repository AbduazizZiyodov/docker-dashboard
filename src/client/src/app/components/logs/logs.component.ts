import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ContainerService } from '@services/container.service';

@Component({
  selector: 'app-logs-modal',
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.scss'],
})
export class LogsComponent implements OnInit {
  logs: string = '';
  container_id: string = this.route.snapshot.params['id'];
  constructor(
    private containerService: ContainerService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.containerService
      .getLogs(this.container_id)
      .subscribe((response: any) => {
        this.logs = response['logs'];
      });
  }
}
