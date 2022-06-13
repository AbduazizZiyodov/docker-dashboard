import { Image } from '@models/image';
import { Container } from '@models/container';
import { MdbModalRef } from 'mdb-angular-ui-kit/modal';

export interface ModalData {
  title?: string;
  modalRef?: MdbModalRef<any>;
  resource?: Image | Container;
  containers?: Container[];

  is_container_modal?: boolean;
  is_delete_image_modal?: boolean;
  is_delete_container_modal?: boolean;
}
