import { Image } from '@models/image';
import { Container } from '@models/container';
import { MdbModalRef } from 'mdb-angular-ui-kit/modal';

export interface ModalData {
  title?: string;
  modalRef?: MdbModalRef<any>;
  resource?: Image | Container;
  containers?: Container[];
  modal_type: string;
}
