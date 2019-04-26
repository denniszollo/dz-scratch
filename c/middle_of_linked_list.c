#include <stdio.h>


struct list
{
  int this;
  struct list* next;
};

struct list* find_middle(struct list * head)
{
  struct list* slow_pointer = head;
  struct list* fast_pointer = head;

  
  if (head == NULL)
  {
    return 0; // 0 is the middle of a 0 length array I guess?
  }

  // I am going to increment fast_pointer twice as fast as slow pointer, when fast pointer hits the end of the linked list, then the slow pointer is basically "half way through"

  while(1)
  {
    // we checked fast pointer for null on the last iteration or before entering loop.
    fast_pointer = fast_pointer->next;
    if (fast_pointer != NULL) 
    {
      fast_pointer = fast_pointer->next;
    }
    else
    {
    //if fast pointer was already ate the end of linked list, than slow pointer is already at middle 
      break;
    }
    // if fast pointer is now at null after getting next, we still return slow pointer as we will 
    // "round down" to middle of list
    if (fast_pointer == NULL)
    {
      break;
    }
    // By this point the fast pointer has incremented twice, so we increment slow pointer and continue
    // No need to check for NULL on slow pointer since it is following the fast one
    slow_pointer = slow_pointer->next;
  }
  return slow_pointer;
}


void main() {
  struct list head, middle, middle2, middle3, end;
  head.this = 0;
  middle.this = 1;
  middle2.this = 2;
  middle3.this = 3;
  end.this = 4;
  head.next = &middle;
  middle.next = &middle2;
  middle2.next = &middle3;
  middle3.next = &end;
  end.next = NULL;

  struct list* middle_of_list;
  middle_of_list = find_middle(&head);
  printf("middle this is %d", middle_of_list->this);
}