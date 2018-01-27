#include <termios.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

#define BAUDRATE B115200
#define dev "/dev/cu.usbserial-A600MICX"
#include "sbp.h"
#include "settings.h"

/*this example sends the following string as SBP payload to the serial port
"surveyed_position\0surveyed_lat\0" + "37" + "\0"
the msg type is the settings write msg
sender id is 0x42 per the spec

make like this: gcc -I../libsbp/c/include/libsbp ../libsbp/c/build/src/libsbp-static.a settings_send.c
*/

static int fd;
static sbp_state_t sbp_state;

static u32 serial_write( u8 *buff, u32 n, void *context )
{
   unsigned int bytes_written = 0;

   bytes_written = write( fd, buff, n );

  return bytes_written;

} // serial_write()

int main(void)
{
    struct termios old_termios;
    struct termios new_termios;

    fd = open(dev, O_RDWR | O_NOCTTY | O_NDELAY);
    fflush(stdout);
    if (fd < 0) {
        fprintf(stderr, "error, counldn't open file %s\n", dev);
        return 1;
    }
    if (tcgetattr(fd, &old_termios) != 0) {
        fprintf(stderr, "tcgetattr(fd, &old_termios) failed: %s\n", strerror(errno));
        return 1;
    }
    memset(&new_termios, 0, sizeof(new_termios));
    new_termios.c_iflag = IGNPAR;
    new_termios.c_oflag = 0;
    new_termios.c_cflag = CS8 | CREAD | CLOCAL | HUPCL;
    new_termios.c_lflag = 0;
    new_termios.c_cc[VINTR]    = 0;
    new_termios.c_cc[VQUIT]    = 0;
    new_termios.c_cc[VERASE]   = 0;
    new_termios.c_cc[VKILL]    = 0;
    new_termios.c_cc[VEOF]     = 4;
    new_termios.c_cc[VTIME]    = 0;
    new_termios.c_cc[VMIN]     = 1;
    new_termios.c_cc[VSTART]   = 0;
    new_termios.c_cc[VSTOP]    = 0;
    new_termios.c_cc[VSUSP]    = 0;
    new_termios.c_cc[VEOL]     = 0;
    new_termios.c_cc[VREPRINT] = 0;
    new_termios.c_cc[VDISCARD] = 0;
    new_termios.c_cc[VWERASE]  = 0;
    new_termios.c_cc[VLNEXT]   = 0;
    new_termios.c_cc[VEOL2]    = 0;

    if (cfsetispeed(&new_termios, BAUDRATE) != 0) {
        fprintf(stderr, "cfsetispeed failed: %s\n", strerror(errno));
        return 1;
    }
    if (cfsetospeed(&new_termios, BAUDRATE) != 0) {
        fprintf(stderr, "cfsetospeed failed: %s\n", strerror(errno));
        return 1;
    }
    if (tcsetattr(fd, TCSANOW, &new_termios) != 0) {
        fprintf(stderr, "tcsetattr(fd, TCSANOW, &new_termios) failed: %s\n", strerror(errno));
        return 1;
    }

    sbp_state_init( &sbp_state );
   
    char   cfg_position[] =  { 's','u','r','v','e','y','e','d','_','p','o','s','i','t','i','o','n','\0', 
                               's','u','r','v','e','y','e','d','_','l','a','t','\0', 
                               '3','7','\0' };
  
    sbp_send_message( &sbp_state, SBP_MSG_SETTINGS_WRITE, 0x42, sizeof(cfg_position),  (u8*) &cfg_position, serial_write );
    return 0; 
}
