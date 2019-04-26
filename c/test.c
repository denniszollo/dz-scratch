#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "libsbp/sbp.h"
#include "libsbp/observation.h"
#include "libsbp/system.h"

#define MAX_NUM_OBS 12
#define MAX_SIDS 32
/* global state */

static sbp_msg_callbacks_node_t obs_callback_node;
packed_obs_content_t curr_obs_array[MAX_NUM_OBS];
int		current_wn = 0;

void obs_callback(u16 sender_id, u8 len, u8 msg[], void *context)
{ static u8 prev_obs_counter;
  static u8	obs_counter; /*keeps track of where in the global array of observations we should be*/
  static u32	prev_head_tow; /*store the TOW of the last message with packet count 0 to guard against skips*/
  static int first = 1;
  static u8 previous_index = 0;
  int num_obs_packets = 0;
	u8		current_index;  /*current packet counter*/
	(void) context;
	if (sender_id != 0) { /*only do things for non-forwarded observations*/
	  /*cast the msg*/
		msg_obs_t      *obs = (msg_obs_t *) msg;
		/* get packet sequence number */
		current_index = obs->header.n_obs & ((1 << 4) - 1);
		/*c alculate the number of obs in this message */
		u8  obs_in_msg = (len - sizeof(observation_header_t)) / sizeof(packed_obs_content_t);
		/* calculate the number of packets we expect */
		num_obs_packets = (obs->header.n_obs >> 4);
		if (current_index == 0) { /* head of a sequence */
      memset(&curr_obs_array, 0, MAX_NUM_OBS * sizeof(packed_obs_content_t)); /* zero our global array */
			memcpy(&curr_obs_array, &obs->obs, obs_in_msg * sizeof(packed_obs_content_t)); /* copy into our array */
      obs_counter=obs_in_msg;
      prev_head_tow = obs->header.t.tow;
      /* if we only have one packet, we have the complete set */
      if(num_obs_packets == 1) {
        printf("we have a complete set, now do something\n");
      }
		}
		/* if the time of week is the same from the last header and we didn't skip a packet, update our obs
            previous header tow   current tow      previous counter + 1 current counter */
		else if (prev_head_tow == obs->header.t.tow && previous_index + 1 == current_index) {
			memcpy(&curr_obs_array[obs_counter],  &obs->obs, obs_in_msg * sizeof(packed_obs_content_t));
			obs_counter += obs_in_msg;
			/* when we get through to the end of the sequence, we do something with the whole set */
			if (num_obs_packets - 1 == current_index) {
       printf("we have a complete set of observations, now lets do something\n");
			}
		}
		previous_index = current_index;
  }
}


u32 stdin_port_read(u8 * buff, u32 n, void *context)
{
	(void)context;
	size_t		num_read;
	num_read = fread(buff, sizeof(u8), n, stdin);
	return num_read;
}


int main()
{
	/*
	 * Takes in one byte at a time from STDIN When it gets a
	 * valid set of observations in sbp it prints something.
	 * Reads MsgObservation only
	 */

	sbp_state_t	s;
	sbp_state_init(&s);

	sbp_register_callback(&s, SBP_MSG_OBS, &obs_callback, NULL,
			      &obs_callback_node);

	while (1) {
		sbp_process(&s, &stdin_port_read);
	}
}
