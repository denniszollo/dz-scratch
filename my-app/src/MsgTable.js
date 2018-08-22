var SbpMsgTable = [
{"257":
{msgName: "MSG_EXT_EVENT", 
msgLen: "12",
shortDesc:"Reports timestamped external pin event",
longDesc:"Reports detection of an external event, the GPS time it occurred, which pin it was and whether it was rising or falling. "}},
{"2304":
{msgName: "MSG_IMU_RAW", 
msgLen: "17",
shortDesc:"Raw IMU data",
longDesc:"Raw data from the Inertial Measurement Unit, containing accelerometer and gyroscope readings. The sense of the measurements are to be aligned with  the indications on the device itself. "}},
{"2305":
{msgName: "MSG_IMU_AUX", 
msgLen: "4",
shortDesc:"Auxiliary IMU data",
longDesc:"Auxiliary data specific to a particular IMU. The `imu\_type` field will always be consistent but the rest of the payload is device specific and depends on the value of `imu\_type`. "}},
{"1025":
{msgName: "MSG_LOG", 
msgLen: "N+1",
shortDesc:"Plaintext logging messages with levels",
longDesc:"This message contains a human-readable payload string from the device containing errors, warnings and informational messages at ERROR, WARNING, DEBUG, INFO logging levels. "}},
{"1026":
{msgName: "MSG_FWD", 
msgLen: "N+2",
shortDesc:"Wrapper for FWD a separate stream of information over SBP",
longDesc:"This message provides the ability to forward messages over SBP.  This may take the form of wrapping up SBP messages received by Piksi for logging purposes or wrapping  another protocol with SBP.\\nThe source identifier indicates from what interface a forwarded stream derived. The protocol identifier identifies what the expected protocol the forwarded msg contains. Protocol 0 represents SBP and the remaining values are implementation defined. "}},
{"2306":
{msgName: "MSG_MAG_RAW", 
msgLen: "11",
shortDesc:"Raw magnetometer data",
longDesc:"Raw data from the magnetometer. "}},
{"258":
{msgName: "MSG_GPS_TIME", 
msgLen: "11",
shortDesc:"GPS Time",
longDesc:"This message reports the GPS time, representing the time since the GPS epoch began on midnight January 6, 1980 UTC. GPS time counts the weeks and seconds of the week. The weeks begin at the Saturday/Sunday transition. GPS week 0 began at the beginning of the GPS time scale.\\nWithin each week number, the GPS time of the week is between between 0 and 604800 seconds (=60*60*24*7). Note that GPS time does not accumulate leap seconds, and as of now, has a small offset from UTC. In a message stream, this message precedes a set of other navigation messages referenced to the same time (but lacking the ns field) and indicates a more precise time of these messages. "}},
{"259":
{msgName: "MSG_UTC_TIME", 
msgLen: "16",
shortDesc:"UTC Time",
longDesc:"This message reports the Universal Coordinated Time (UTC).  Note the flags which indicate the source of the UTC offset value and source of the time fix. "}},
{"520":
{msgName: "MSG_DOPS", 
msgLen: "15",
shortDesc:"Dilution of Precision",
longDesc:"This dilution of precision (DOP) message describes the effect of navigation satellite geometry on positional measurement precision.  The flags field indicated whether the DOP reported corresponds to differential or SPP solution. "}},
{"521":
{msgName: "MSG_POS_ECEF", 
msgLen: "32",
shortDesc:"Single-point position in ECEF",
longDesc:"The position solution message reports absolute Earth Centered Earth Fixed (ECEF) coordinates and the status (single point vs pseudo-absolute RTK) of the position solution. If the rover receiver knows the surveyed position of the base station and has an RTK solution, this reports a pseudo-absolute position solution using the base station position and the rover's RTK baseline vector. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"532":
{msgName: "MSG_POS_ECEF_COV", 
msgLen: "54",
shortDesc:"Single-point position in ECEF",
longDesc:"The position solution message reports absolute Earth Centered Earth Fixed (ECEF) coordinates and the status (single point vs pseudo-absolute RTK) of the position solution. The message also reports the upper triangular portion of the 3x3 covariance matrix. If the receiver knows the surveyed position of the base station and has an RTK solution, this reports a pseudo-absolute position solution using the base station position and the rover's RTK baseline vector. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"522":
{msgName: "MSG_POS_LLH", 
msgLen: "34",
shortDesc:"Geodetic Position",
longDesc:"This position solution message reports the absolute geodetic coordinates and the status (single point vs pseudo-absolute RTK) of the position solution. If the rover receiver knows the surveyed position of the base station and has an RTK solution, this reports a pseudo-absolute position solution using the base station position and the rover's RTK baseline vector. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"529":
{msgName: "MSG_POS_LLH_COV", 
msgLen: "54",
shortDesc:"Geodetic Position",
longDesc:"This position solution message reports the absolute geodetic coordinates and the status (single point vs pseudo-absolute RTK) of the position solution as well as the upper triangle of the 3x3 covariance matrix.  The position information and Fix Mode flags should follow the MSG\_POS\_LLH message.  Since the covariance matrix is computed in the local-level North, East, Down frame, the covariance terms follow with that convention. Thus, covariances are reported against the \\''downward\\'' measurement and care should be taken with the sign convention. "}},
{"523":
{msgName: "MSG_BASELINE_ECEF", 
msgLen: "20",
shortDesc:"Baseline Position in ECEF",
longDesc:"This message reports the baseline solution in Earth Centered Earth Fixed (ECEF) coordinates. This baseline is the relative vector distance from the base station to the rover receiver. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"524":
{msgName: "MSG_BASELINE_NED", 
msgLen: "22",
shortDesc:"Baseline in NED",
longDesc:"This message reports the baseline solution in North East Down (NED) coordinates. This baseline is the relative vector distance from the base station to the rover receiver, and NED coordinate system is defined at the local WGS84 tangent plane centered at the base station position.  The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"525":
{msgName: "MSG_VEL_ECEF", 
msgLen: "20",
shortDesc:"Velocity in ECEF",
longDesc:"This message reports the velocity in Earth Centered Earth Fixed (ECEF) coordinates. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"533":
{msgName: "MSG_VEL_ECEF_COV", 
msgLen: "42",
shortDesc:"Velocity in ECEF",
longDesc:"This message reports the velocity in Earth Centered Earth Fixed (ECEF) coordinates. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"526":
{msgName: "MSG_VEL_NED", 
msgLen: "22",
shortDesc:"Velocity in NED",
longDesc:"This message reports the velocity in local North East Down (NED) coordinates. The NED coordinate system is defined as the local WGS84 tangent plane centered at the current position. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"530":
{msgName: "MSG_VEL_NED_COV", 
msgLen: "42",
shortDesc:"Velocity in NED",
longDesc:"This message reports the velocity in local North East Down (NED) coordinates. The NED coordinate system is defined as the local WGS84 tangent plane centered at the current position. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). This message is similar to the MSG\_VEL\_NED, but it includes the upper triangular portion of the 3x3 covariance matrix. "}},
{"531":
{msgName: "MSG_VEL_BODY", 
msgLen: "42",
shortDesc:"Velocity in User Frame",
longDesc:"This message reports the velocity in the Vehicle Body Frame. By convention, the x-axis should point out the nose of the vehicle and represent the forward direction, while as the y-axis should point out the right hand side of the vehicle. Since this is a right handed system, z should point out the bottom of the vehicle. The orientation and origin of the Vehicle Body Frame are specified via the device settings. The full GPS time is given by the preceding MSG\_GPS\_TIME with the matching time-of-week (tow). "}},
{"528":
{msgName: "MSG_AGE_CORRECTIONS", 
msgLen: "6",
shortDesc:"Age of corrections",
longDesc:"This message reports the Age of the corrections used for the current Differential solution "}},
{"74":
{msgName: "MSG_OBS", 
msgLen: "17N+11",
shortDesc:"GPS satellite observations",
longDesc:"The GPS observations message reports all the raw pseudorange and carrier phase observations for the satellites being tracked by the device. Carrier phase observation here is represented as a 40-bit fixed point number with Q32.8 layout (i.e. 32-bits of whole cycles and 8-bits of fractional cycles). The observations are be interoperable with 3rd party receivers and conform with typical RTCMv3 GNSS observations. "}},
{"68":
{msgName: "MSG_BASE_POS_LLH", 
msgLen: "24",
shortDesc:"Base station position",
longDesc:"The base station position message is the position reported by the base station itself. It is used for pseudo-absolute RTK positioning, and is required to be a high-accuracy surveyed location of the base station. Any error here will result in an error in the pseudo-absolute position output. "}},
{"72":
{msgName: "MSG_BASE_POS_ECEF", 
msgLen: "24",
shortDesc:"Base station position in ECEF",
longDesc:"The base station position message is the position reported by the base station itself in absolute Earth Centered Earth Fixed coordinates. It is used for pseudo-absolute RTK positioning, and is required to be a high-accuracy surveyed location of the base station. Any error here will result in an error in the pseudo-absolute position output. "}},
{"129":
{msgName: "MSG_EPHEMERIS_GPS_DEP_E", 
msgLen: "185",
shortDesc:"Satellite broadcast ephemeris for GPS",
longDesc:"The ephemeris message returns a set of satellite orbit parameters that is used to calculate GPS satellite position, velocity, and clock offset. Please see the Navstar GPS Space Segment/Navigation user interfaces (ICD-GPS-200, Table 20-III) for more details. "}},
{"134":
{msgName: "MSG_EPHEMERIS_GPS_DEP_F", 
msgLen: "183",
shortDesc:"Deprecated",
longDesc:"This observation message has been deprecated in favor of ephemeris message using floats for size reduction. "}},
{"138":
{msgName: "MSG_EPHEMERIS_GPS", 
msgLen: "139",
shortDesc:"Satellite broadcast ephemeris for GPS",
longDesc:"The ephemeris message returns a set of satellite orbit parameters that is used to calculate GPS satellite position, velocity, and clock offset. Please see the Navstar GPS Space Segment/Navigation user interfaces (ICD-GPS-200, Table 20-III) for more details. "}},
{"137":
{msgName: "MSG_EPHEMERIS_BDS", 
msgLen: "147",
shortDesc:"Satellite broadcast ephemeris for BDS",
longDesc:"The ephemeris message returns a set of satellite orbit parameters that is used to calculate BDS satellite position, velocity, and clock offset. Please see the BeiDou Navigation Satellite System SIS-ICD Version 2.1, Table 5-9 for more details. "}},
{"149":
{msgName: "MSG_EPHEMERIS_GAL", 
msgLen: "152",
shortDesc:"Satellite broadcast ephemeris for Galileo",
longDesc:"The ephemeris message returns a set of satellite orbit parameters that is used to calculate Galileo satellite position, velocity, and clock offset. Please see the Signal In Space ICD OS SIS ICD, Issue 1.3, December 2016 for more details. "}},
{"130":
{msgName: "MSG_EPHEMERIS_SBAS_DEP_A", 
msgLen: "112",
shortDesc:"Satellite broadcast ephemeris for SBAS",
longDesc:""}},
{"131":
{msgName: "MSG_EPHEMERIS_GLO_DEP_A", 
msgLen: "112",
shortDesc:"Satellite broadcast ephemeris for GLO",
longDesc:"The ephemeris message returns a set of satellite orbit parameters that is used to calculate GLO satellite position, velocity, and clock offset. Please see the GLO ICD 5.1 \\''Table 4.5 Characteristics of words of immediate information (ephemeris parameters)\\'' for more details. "}},
{"132":
{msgName: "MSG_EPHEMERIS_SBAS_DEP_B", 
msgLen: "110",
shortDesc:"Deprecated",
longDesc:"This observation message has been deprecated in favor of ephemeris message using floats for size reduction. "}},
{"140":
{msgName: "MSG_EPHEMERIS_SBAS", 
msgLen: "74",
shortDesc:"Satellite broadcast ephemeris for SBAS",
longDesc:""}},
{"133":
{msgName: "MSG_EPHEMERIS_GLO_DEP_B", 
msgLen: "110",
shortDesc:"Satellite broadcast ephemeris for GLO",
longDesc:"The ephemeris message returns a set of satellite orbit parameters that is used to calculate GLO satellite position, velocity, and clock offset. Please see the GLO ICD 5.1 \\''Table 4.5 Characteristics of words of immediate information (ephemeris parameters)\\'' for more details. "}},
{"135":
{msgName: "MSG_EPHEMERIS_GLO_DEP_C", 
msgLen: "119",
shortDesc:"Satellite broadcast ephemeris for GLO",
longDesc:"The ephemeris message returns a set of satellite orbit parameters that is used to calculate GLO satellite position, velocity, and clock offset. Please see the GLO ICD 5.1 \\''Table 4.5 Characteristics of words of immediate information (ephemeris parameters)\\'' for more details. "}},
{"136":
{msgName: "MSG_EPHEMERIS_GLO_DEP_D", 
msgLen: "120",
shortDesc:"Deprecated",
longDesc:"This observation message has been deprecated in favor of ephemeris message using floats for size reduction. "}},
{"139":
{msgName: "MSG_EPHEMERIS_GLO", 
msgLen: "92",
shortDesc:"Satellite broadcast ephemeris for GLO",
longDesc:"The ephemeris message returns a set of satellite orbit parameters that is used to calculate GLO satellite position, velocity, and clock offset. Please see the GLO ICD 5.1 \\''Table 4.5 Characteristics of words of immediate information (ephemeris parameters)\\'' for more details. "}},
{"144":
{msgName: "MSG_IONO", 
msgLen: "70",
shortDesc:"Iono corrections",
longDesc:"The ionospheric parameters which allow the \\''L1 only\\'' or \\''L2 only\\'' user to utilize the ionospheric model for computation of the ionospheric delay. Please see ICD-GPS-200 (Chapter 20.3.3.5.1.7) for more details. "}},
{"145":
{msgName: "MSG_SV_CONFIGURATION_GPS_DEP", 
msgLen: "10",
shortDesc:"L2C capability mask",
longDesc:"Please see ICD-GPS-200 (Chapter 20.3.3.5.1.4) for more details. "}},
{"150":
{msgName: "MSG_GNSS_CAPB", 
msgLen: "110",
shortDesc:"GNSS capabilities",
longDesc:""}},
{"146":
{msgName: "MSG_GROUP_DELAY_DEP_A", 
msgLen: "14",
shortDesc:"Group Delay",
longDesc:"Please see ICD-GPS-200 (30.3.3.3.1.1) for more details."}},
{"147":
{msgName: "MSG_GROUP_DELAY_DEP_B", 
msgLen: "17",
shortDesc:"Group Delay",
longDesc:"Please see ICD-GPS-200 (30.3.3.3.1.1) for more details."}},
{"148":
{msgName: "MSG_GROUP_DELAY", 
msgLen: "15",
shortDesc:"Group Delay",
longDesc:"Please see ICD-GPS-200 (30.3.3.3.1.1) for more details."}},
{"114":
{msgName: "MSG_ALMANAC_GPS", 
msgLen: "94",
shortDesc:"Satellite broadcast ephemeris for GPS",
longDesc:"The almanac message returns a set of satellite orbit parameters. Almanac data is not very precise and is considered valid for up to several months. Please see the Navstar GPS Space Segment/Navigation user interfaces (ICD-GPS-200, Chapter 20.3.3.5.1.2 Almanac Data) for more details. "}},
{"115":
{msgName: "MSG_ALMANAC_GLO", 
msgLen: "78",
shortDesc:"Satellite broadcast ephemeris for GLO",
longDesc:"The almanac message returns a set of satellite orbit parameters. Almanac data is not very precise and is considered valid for up to several months. Please see the GLO ICD 5.1 \\''Chapter 4.5 Non-immediate information and almanac\\'' for details. "}},
{"117":
{msgName: "MSG_GLO_BIASES", 
msgLen: "9",
shortDesc:"GLONASS L1/L2 Code-Phase biases",
longDesc:"The GLONASS L1/L2 Code-Phase biases allows to perform GPS+GLONASS integer ambiguity resolution for baselines with mixed receiver types (e.g. receiver of different manufacturers) "}},
{"161":
{msgName: "MSG_SETTINGS_SAVE", 
msgLen: "0",
shortDesc:"Save settings to flash (host => device)",
longDesc:"The save settings message persists the device's current settings configuration to its onboard flash memory file system. "}},
{"160":
{msgName: "MSG_SETTINGS_WRITE", 
msgLen: "N",
shortDesc:"Write device configuration settings (host => device)",
longDesc:"The setting message writes the device configuration for a particular setting via A NULL-terminated and NULL-delimited string with contents \\''SECTION\_SETTING\\0SETTING\\0VALUE\\0\\'' where the '\\0' escape sequence denotes  the NULL character and where quotation marks are omitted. A device will only process to this message when it is received from sender ID 0x42. An example string that could be sent to a device is \\''solution\\0soln\_freq\\010\\0\\''. "}},
{"175":
{msgName: "MSG_SETTINGS_WRITE_RESP", 
msgLen: "N+1",
shortDesc:"Acknowledgement with status of MSG\_SETTINGS\_WRITE",
longDesc:"Return the status of a write request with the new value of the setting.  If the requested value is rejected, the current value will be returned. The string field is a NULL-terminated and NULL-delimited string with contents \\''SECTION\_SETTING\\0SETTING\\0VALUE\\0\\'' where the '\\0' escape sequence denotes the NULL character and where quotation marks are omitted. An example string that could be sent from device is \\''solution\\0soln\_freq\\010\\0\\''. "}},
{"164":
{msgName: "MSG_SETTINGS_READ_REQ", 
msgLen: "N",
shortDesc:"Read device configuration settings (host => device)",
longDesc:"The setting message that reads the device configuration. The string field is a NULL-terminated and NULL-delimited string with contents \\''SECTION\_SETTING\\0SETTING\\0\\'' where the '\\0' escape sequence denotes the NULL character and where quotation marks are omitted. An example string that could be sent to a device is \\''solution\\0soln\_freq\\0\\''. A device will only respond to this message when it is received from sender ID 0x42. A device should respond with a MSG\_SETTINGS\_READ\_RESP message (msg\_id 0x00A5). "}},
{"165":
{msgName: "MSG_SETTINGS_READ_RESP", 
msgLen: "N",
shortDesc:"Read device configuration settings (host <= device)",
longDesc:"The setting message wich which the device responds after a MSG\_SETTING\_READ\_REQ is sent to device. The string field is a NULL-terminated and NULL-delimited string with contents \\''SECTION\_SETTING\\0SETTING\\0VALUE\\0\\'' where the '\\0' escape sequence denotes the NULL character and where quotation marks are omitted. An example string that could be sent from device is \\''solution\\0soln\_freq\\010\\0\\''. "}},
{"162":
{msgName: "MSG_SETTINGS_READ_BY_INDEX_REQ", 
msgLen: "2",
shortDesc:"Read setting by direct index (host => device)",
longDesc:"The settings message for iterating through the settings values. A device will respond to this message with a  \\''MSG\_SETTINGS\_READ\_BY\_INDEX\_RESP\\''. "}},
{"167":
{msgName: "MSG_SETTINGS_READ_BY_INDEX_RESP", 
msgLen: "N+2",
shortDesc:"Read setting by direct index (host <= device)",
longDesc:"The settings message that reports the value of a setting at an index.\\nIn the string field, it reports NULL-terminated and delimited string with contents \\''SECTION\_SETTING\\0SETTING\\0VALUE\\0FORMAT\_TYPE\\0\\''. where the '\\0' escape sequence denotes the NULL character and where quotation marks are omitted. The FORMAT\_TYPE field is optional and denotes possible string values of the setting as a hint to the user. If included, the format type portion of the string has the format \\''enum:value1,value2,value3\\''. An example string that could be sent from the device is \\''simulator\\0enabled\\0True\\0enum:True,False\\0\\'' "}},
{"166":
{msgName: "MSG_SETTINGS_READ_BY_INDEX_DONE", 
msgLen: "0",
shortDesc:"Finished reading settings (host <= device)",
longDesc:"The settings message for indicating end of the settings values. "}},
{"65280":
{msgName: "MSG_STARTUP", 
msgLen: "4",
shortDesc:"System start-up message",
longDesc:"The system start-up message is sent once on system start-up. It notifies the host or other attached devices that the system has started and is now ready to respond to commands or configuration requests. "}},
{"65282":
{msgName: "MSG_DGNSS_STATUS", 
msgLen: "N+4",
shortDesc:"Status of received corrections",
longDesc:"This message provides information about the receipt of Differential corrections.  It is expected to be sent with each receipt of a complete corrections packet. "}},
{"65535":
{msgName: "MSG_HEARTBEAT", 
msgLen: "4",
shortDesc:"System heartbeat message",
longDesc:"The heartbeat message is sent periodically to inform the host or other attached devices that the system is running. It is used to monitor system malfunctions. It also contains status flags that indicate to the host the status of the system and whether it is operating correctly. Currently, the expected heartbeat interval is 1 sec.\\nThe system error flag is used to indicate that an error has occurred in the system. To determine the source of the error, the remaining error flags should be inspected. "}},
{"65283":
{msgName: "MSG_INS_STATUS", 
msgLen: "4",
shortDesc:"Inertial Navigation System status message",
longDesc:"The INS status message describes the state of the operation and initialization of the inertial navigation system.  "}},]
export {SbpMsgTable}