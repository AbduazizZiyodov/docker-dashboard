import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImageDetailedComponent } from './image-detailed.component';

describe('ImageDetailedComponent', () => {
  let component: ImageDetailedComponent;
  let fixture: ComponentFixture<ImageDetailedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ImageDetailedComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ImageDetailedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
