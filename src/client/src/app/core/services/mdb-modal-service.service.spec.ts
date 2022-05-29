import { TestBed } from '@angular/core/testing';

import { MdbModalServiceService } from './mdb-modal-service.service';

describe('MdbModalServiceService', () => {
  let service: MdbModalServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MdbModalServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
