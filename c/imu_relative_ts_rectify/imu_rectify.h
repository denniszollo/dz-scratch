/*
 * smoothpose_runner.h
 *
 *  Created on: Jun 26, 2019
 *      Author: dzollo
 */

#ifndef SRC_SMOOTHPOSE_RUNNER_H_
#define SRC_SMOOTHPOSE_RUNNER_H_

#ifdef __cplusplus
extern "C" {
#endif

#include "libsbp/sbp.h"
#include "libsbp/common.h"

sbp_state_t out_context;
int imu_rectify(char* infile_name, char* outfile_name);
s32 file_write(u8 * buff, u32 n, void *context);
void runner_exit();

#ifdef __cplusplus
}
#endif

#endif /* SRC_SMOOTHPOSE_RUNNER_H_ */
