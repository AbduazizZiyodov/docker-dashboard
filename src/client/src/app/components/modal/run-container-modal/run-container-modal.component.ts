import { Router } from '@angular/router';
import { Component, Input, OnInit } from '@angular/core';
import { FormArray, FormBuilder, FormGroup, Validators } from '@angular/forms';

import { ToastrService } from 'ngx-toastr';
import { ModalData } from '@models/modal';
import { ContainerService } from '@services/container.service';
import { Container } from '@models/container';

@Component({
  selector: 'app-run-container-modal',
  templateUrl: './run-container-modal.component.html',
  styleUrls: ['./run-container-modal.component.scss'],
})
export class RunContainerModalComponent implements OnInit {
  runContainerForm!: FormGroup;
  @Input() data!: ModalData;

  constructor(
    private formBuilder: FormBuilder,
    private router: Router,
    private toastr: ToastrService,
    private containerService: ContainerService
  ) {}

  ngOnInit(): void {
    this.runContainerForm = this.formBuilder.group({
      name: null,
      entrypoint: null,
      command: null,
      firstPort: null,
      secondPort: null,
      env: this.formBuilder.array([]),
    });
  }

  formSubmit() {
    this.toastr.warning("Running ...")
    this.containerService
      .runContainer(this.getContainerData())
      .subscribe((container: Container) => {
        this.data.modalRef?.close();
        this.toastr.success('Success!');
        this.router.navigate(['containers']);
      });
  }

  getContainerData() {
    let containerData = this.runContainerForm.getRawValue();

    let firstPort = containerData.firstPort,
      secondPort = containerData.secondPort;

    containerData['ports'] = {};
    containerData['environment'] = {};

    containerData['image'] = this.data.resource?.name;

    if (firstPort && secondPort) {
      containerData['ports'][firstPort] = secondPort;
    }

    for (let environmentVariable of containerData.env) {
      containerData['environment'][environmentVariable.key] =
        environmentVariable.value;
    }

    for (let key of ['env', 'firstPort', 'secondPort']) {
      delete containerData[key];
    }

    console.log(containerData);

    return containerData;
  }

  newEnvironmentVariable(): FormGroup {
    return this.formBuilder.group({
      key: '',
      value: '',
    });
  }

  addEnvironmentVariable() {
    this.environment().push(this.newEnvironmentVariable());
  }

  removeEnvironmentVariable(index: number) {
    this.environment().removeAt(index);
  }

  environment(): FormArray {
    return this.runContainerForm.get('env') as FormArray;
  }

  get name() {
    return this.runContainerForm.get('name');
  }
  get entrypoint() {
    return this.runContainerForm.get('entrypoint');
  }

  get firstPort() {
    return this.runContainerForm.get('firstPort');
  }
  get secondPort() {
    return this.runContainerForm.get('secondPort');
  }
}
