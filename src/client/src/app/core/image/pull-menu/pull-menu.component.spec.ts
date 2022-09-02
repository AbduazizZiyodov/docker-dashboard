import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PullMenuComponent } from './pull-menu.component';

describe('PullMenuComponent', () => {
  let component: PullMenuComponent;
  let fixture: ComponentFixture<PullMenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PullMenuComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PullMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
