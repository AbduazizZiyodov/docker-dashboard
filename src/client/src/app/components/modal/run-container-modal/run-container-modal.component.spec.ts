import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunContainerModalComponent } from './run-container-modal.component';

describe('RunContainerModalComponent', () => {
  let component: RunContainerModalComponent;
  let fixture: ComponentFixture<RunContainerModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RunContainerModalComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RunContainerModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
