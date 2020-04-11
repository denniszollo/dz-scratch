#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include "libsbp/navigation.h"
#include "libsbp/vehicle.h"
#include "libsbp/sbp.h"
#include "libsbp/imu.h"
#include "libsbp/edc.h"

#include "imu_rectify.h"

#define DEBUG 1
#define SBP_PREAMBLE 0x55

#define WRITE_ATTEMPTS 10
#define READ_ATTEMPTS 10

FILE *infd = NULL;
FILE *outfd = NULL;

s32 file_read(u8 * buff, u32 n, void *context) {
    (void) context;
    size_t num_bytes = 0;
    static int num_failures = 0;
    num_bytes = fread(buff, 1, n, infd);
    if (num_bytes == 0) {
        if (DEBUG) {
            printf("read: %lu, requested %d\n", num_bytes, n);
        }
        num_failures++;
    }
    else{
      num_failures = 0;
    }
    if(num_failures > READ_ATTEMPTS) {
        if (DEBUG) {
            printf("read: %lu, requested %d\n", num_bytes, n);
        }
        runner_exit();
    }
    return num_bytes;
}

s32 file_write(u8 * buff, u32 n, void *context) {
    (void) context;
    size_t num_bytes = 0;
    static int num_failures = 0;
    num_bytes = fwrite(buff, 1, n, outfd);
    if (num_bytes != n) {
        if (DEBUG) {
            printf("wrote: %lu, requested %u\n", num_bytes, n);
        }
        num_failures++;
    }
    else{
      num_failures = 0;
    }
    if(num_failures > WRITE_ATTEMPTS) {
        printf("Issue writing %u bytes to SBP outfile. Only %lu bytes written. Exiting.\n", n,
                num_bytes);
        exit(1);
    }
    return num_bytes;
}

/** Directly process a SBP message.
 * If a SBP message has already been decoded (for example, from a binary
 * stream or from a JSON log file) use this function to directly process it.
 *
 * \param s State structure
 * \param sender_id SBP message sender id
 * \param msg_type SBP message type
 * \param msg_len SBP message length
 * \param payload SBP message payload
 * \return `SBP_OK_CALLBACK_EXECUTED` (1) if message decoded and callback executed,
 *         `SBP_OK_CALLBACK_UNDEFINED` (2) if message decoded with no associated
 *         callback.
 */
s8 runner_sbp_process_payload(sbp_state_t *s, u16 sender_id, u16 msg_type, u8 msg_len,
        u8 payload[]) {
    //  static int last_pos_llh_mode = 0;
    static uint32_t current_tow_s = 0;
    static uint32_t last_tow_s = 0;
    static uint32_t last_imu_tow_relative = 0;
    static uint32_t num_rollovers = 0;
    msg_gps_time_t* gps_time_time;
    msg_imu_raw_t* imu_raw;
    switch (msg_type)
    {
    /* GNSS or INS outputs */
    case SBP_MSG_IMU_RAW:      // 0x0900: MSG_IMU_RAW
        imu_raw = (msg_imu_raw_t*) payload;
        if((imu_raw->tow & 0xC0000000) != 0xC0000000 || current_tow_s == 0) {
           if(DEBUG) printf("non relative IMU timestamp detected, not unwrapping anything\n");
           sbp_send_message(s, msg_type, sender_id, msg_len, payload, &file_write);
        }
        else
        {
          uint32_t current_imu_tow_residual = (imu_raw->tow & ~0xC0000000);
          printf("curent residual is %u\n", current_imu_tow_residual);
        if (current_imu_tow_residual < last_imu_tow_relative) // if last tow
        {
          if(DEBUG) printf("rollover detected, adding to rollover counter: %u\n", num_rollovers);
          num_rollovers += 1;
        }
        if (last_tow_s != current_tow_s)
        {
          if(DEBUG) printf("gps_time caught up, resetting rollover counter to 0");
          num_rollovers = 0;
        }
        last_tow_s = current_tow_s;
        if(DEBUG) printf("setting IMU tow to %u\n", current_tow_s + current_imu_tow_residual + num_rollovers * 1000);
        imu_raw->tow = current_tow_s + current_imu_tow_residual + num_rollovers * 1000 ;
        sbp_send_message(s, msg_type, sender_id, msg_len, payload, &file_write);
        last_imu_tow_relative = current_imu_tow_residual;
        }
        break;
    case SBP_MSG_WHEELTICK:      // 0x0903: MSG_ODOMETRY
        //OdometryCallback(sender_id, msg_len, payload, pose);
        sbp_send_message(s, msg_type, sender_id, msg_len, payload, &file_write);
        break;
    case SBP_MSG_GPS_TIME: //0x0209: MSG_POS_ECEF
        {
        gps_time_time = (msg_gps_time_t*) payload;
        if (gps_time_time->flags != 0) {
          uint32_t rounded_tow = gps_time_time->tow +  gps_time_time->ns_residual/1000000.0;
          if (rounded_tow % 1000 == 0)
          {
          if(DEBUG) printf("curent GPS TOW is is %u\n", rounded_tow);
          current_tow_s = rounded_tow;

          }
        ; 
        }
        }// intentionally fall through
    default:
        sbp_send_message(s, msg_type, sender_id, msg_len, payload, &file_write);
    }
    return SBP_OK_CALLBACK_EXECUTED;
}

/*replaces sbp_process so that we can just have generic callback for every SBP message*/

s8 runner_sbp_process(sbp_state_t *s, s32 (*read)(u8 *buff, u32 n, void *context))
{
    /* Sanity checks */
    if ((0 == s) || (0 == read)) {
        return SBP_NULL_ERROR;
    }

    u8 temp;
    u16 crc;
    s32 rd = 0;

    switch (s->state) {
    case WAITING:
        rd = (*read)(&temp, 1, s->io_context);
        if (0 > rd)
            return SBP_READ_ERROR;
        if (1 == rd)
            if (temp == SBP_PREAMBLE) {
                s->n_read = 0;
                s->state = GET_TYPE;
            }
        break;

    case GET_TYPE:
        rd = (*read)((u8*) &(s->msg_type) + s->n_read, 2 - s->n_read, s->io_context);
        if (0 > rd)
            return SBP_READ_ERROR;
        s->n_read += rd;
        if (s->n_read >= 2) {
            /* Swap bytes to little endian. */
            s->n_read = 0;
            s->state = GET_SENDER;
        }
        break;

    case GET_SENDER:
        rd = (*read)((u8*) &(s->sender_id) + s->n_read, 2 - s->n_read, s->io_context);
        if (0 > rd)
            return SBP_READ_ERROR;
        s->n_read += rd;
        if (s->n_read >= 2) {
            /* Swap bytes to little endian. */
            s->state = GET_LEN;
        }
        break;

    case GET_LEN:
        rd = (*read)(&(s->msg_len), 1, s->io_context);
        if (0 > rd)
            return SBP_READ_ERROR;
        if (1 == rd) {
            s->n_read = 0;
            s->state = GET_MSG;
        }
        break;

    case GET_MSG:
        /* Not received whole message yet, try and read some more. */
        rd = (*read)(&(s->msg_buff[s->n_read]), s->msg_len - s->n_read, s->io_context);
        if (0 > rd)
            return SBP_READ_ERROR;
        s->n_read += rd;
        if (s->msg_len - s->n_read <= 0) {
            s->n_read = 0;
            s->state = GET_CRC;
        }
        break;

    case GET_CRC:
        rd = (*read)((u8*) &(s->crc) + s->n_read, 2 - s->n_read, s->io_context);
        if (0 > rd)
            return SBP_READ_ERROR;
        s->n_read += rd;
        if (s->n_read >= 2) {
            s->state = WAITING;

            /* Swap bytes to little endian. */
            crc = crc16_ccitt((u8*) &(s->msg_type), 2, 0);
            crc = crc16_ccitt((u8*) &(s->sender_id), 2, crc);
            crc = crc16_ccitt(&(s->msg_len), 1, crc);
            crc = crc16_ccitt(s->msg_buff, s->msg_len, crc);
            if (s->crc == crc) {

                /* Message complete, process it. */
                if(DEBUG) printf("processing message %u\n", s->msg_type);
                s8 ret = runner_sbp_process_payload(s, s->sender_id, s->msg_type, s->msg_len,
                        s->msg_buff);
                return ret;
            } else {
                return SBP_CRC_ERROR;
            }
        }
        break;

    default:
        s->state = WAITING;
        break;
    }
    return SBP_OK;
}

int imu_rectify(char* infile_name, char* outfile_name) {
    sbp_state_t s;
    sbp_state_init(&s);
    sbp_state_init(&out_context);
    infd = fopen(infile_name, "rb");
    if (infd == NULL) {
      printf("error opening input file");
      fprintf(stderr, "error opening input file");
      return 1;
    }
    outfd = fopen(outfile_name, "wb");
    if (outfd == NULL) {
      printf("error opening output file");
      fprintf(stderr, "error opening output file");
      return 1;
    }
    if (NULL == infd) {
        printf("\nERROR: file %s cannot be opened.\n\n", infile_name);
        return 1;
    }

    while (1) {
        runner_sbp_process(&s, &file_read);
        //usleep(1);
    }

    return 0;
}

void runner_exit() {
    fflush(outfd);
    fclose(outfd);
    fclose(infd);
    exit(0);
}
