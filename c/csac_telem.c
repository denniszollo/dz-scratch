#include <termios.h>
#include <time.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

#define BAUDRATE B57600
#define dev "/dev/cu.usbserial-A700HJDD"
#define DEBUG 0

/*
 * this example sends the following string as SBP payload to the serial port
 * "surveyed_position\0surveyed_lat\0" + "37" + "\0" the msg type is the
 * settings write msg sender id is 0x42 per the spec
 * 
 * make like this: gcc -I../libsbp/c/include/libsbp
 * ../libsbp/c/build/src/libsbp-static.a settings_send.c
 */

static int	fd;


int
read_until_cr_lf(int fd, char *outbuf, size_t maxlen)
{
	int		nbytes;	/* Number of bytes read */
	char           *bufptr;	/* Current char in buffer */
	bufptr = outbuf;
	char           *eob = outbuf + maxlen;
	while ((nbytes = read(fd, bufptr, (size_t) (eob - bufptr) - 1)) > 0) {
		bufptr += nbytes;
		if ((size_t) (bufptr - outbuf) > 2) {
			if (bufptr[-1] == '\n' || bufptr[-2] == '\r') {
				break;
			}
		}
	}
	*bufptr = '\0';
	return (size_t) (bufptr - outbuf);
}

int
main(void)
{
  if (DEBUG)
    printf("running");
  intcycle = 0;     /* cycle_offset for quering column names */
  char buffer[255]; /* Input buffer */
  memset(buffer, 0, 255);
  struct termios old_termios;
  struct termios new_termios;
  fd = open(dev, O_RDWR | O_NOCTTY | O_NDELAY);
  if (DEBUG)
    printf("open");
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
	new_termios.c_cc[VINTR] = 0;
	new_termios.c_cc[VQUIT] = 0;
	new_termios.c_cc[VERASE] = 0;
	new_termios.c_cc[VKILL] = 0;
	new_termios.c_cc[VEOF] = 4;
	new_termios.c_cc[VTIME] = 0;
	new_termios.c_cc[VMIN] = 1;
	new_termios.c_cc[VSTART] = 0;
	new_termios.c_cc[VSTOP] = 0;
	new_termios.c_cc[VSUSP] = 0;
	new_termios.c_cc[VEOL] = 0;
	new_termios.c_cc[VREPRINT] = 0;
	new_termios.c_cc[VDISCARD] = 0;
	new_termios.c_cc[VWERASE] = 0;
	new_termios.c_cc[VLNEXT] = 0;
	new_termios.c_cc[VEOL2] = 0;

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
        if (DEBUG)
          printf("before while");
        while (1) {
          if (DEBUG)
            printf("while");
          fflush(stdout);
          int tries; /* Number of tries so far */
          if (cycle == 0) {
            cycle++;
            for (tries = 0; tries < 10; tries++) {
              if (DEBUG)
                printf("trying headers %d", tries);
              memset(buffer, 0, 255);
              /* send an AT command followed by a CR */
              if (write(fd, "6\r\n", 3) < 3) {
                fprintf(stderr, "less than 3 bytes written\n");
                continue;
              }
              usleep(100000); /* 10 ms */
              /*
               * read characters into our string buffer
               * until we get a CR or NL
               */
              int bytes = read_until_cr_lf(fd, buffer, 255);
              if (DEBUG)
                printf("read %d bytes\n", bytes);
              if (DEBUG)
                printf("%c %c %c : %c %c %c\n", buffer[0], buffer[1], buffer[2],
                       buffer[bytes - 3], buffer[bytes - 4], buffer[bytes - 5]);
              if (bytes > 50) {
                if (buffer[0] == 'S' &&
                    buffer[bytes - 3] == 'r') /* Check first and last characters
                                                 which are known */
                {
                  printf("%s,%s", "cycle,time,", buffer);
                }
                break;
              }
            }
          }
          for (tries = 0; tries < 3; tries++) {
            /* send an AT command followed by a CR */
            if (write(fd, "^\r\n", 3) < 3) {
              fprintf(stderr, "less than 3 bytes written\n");
              continue;
            }
            usleep(100000);
            int bytes = read_until_cr_lf(fd, buffer, 255);
            if (bytes > 50)
              printf("%d,%ld,%s", cycle, time(NULL), buffer);
            break;
          }
          usleep(990000); /* 990 ms */
        }
}
