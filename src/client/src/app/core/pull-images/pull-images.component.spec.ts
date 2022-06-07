import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PullImagesComponent } from './pull-images.component';

describe('PullImagesComponent', () => {
  let component: PullImagesComponent;
  let fixture: ComponentFixture<PullImagesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PullImagesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PullImagesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
