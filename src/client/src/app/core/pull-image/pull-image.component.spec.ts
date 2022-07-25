import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PullImageComponent } from './pull-image.component';

describe('PullImageComponent', () => {
  let component: PullImageComponent;
  let fixture: ComponentFixture<PullImageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PullImageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PullImageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
