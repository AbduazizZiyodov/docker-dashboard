import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateContainersComponent } from './create-containers.component';

describe('CreateContainersComponent', () => {
  let component: CreateContainersComponent;
  let fixture: ComponentFixture<CreateContainersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CreateContainersComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(CreateContainersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
