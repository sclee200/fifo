#include <stdio.h>
#include <sys/types.h>               // 헤더 파일
#include <sys/stat.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

#define  FIFO_FILE   "/tmp/fifo"
#define  BUFF_SIZE   1024

int main( void)
{
   int   counter = 0;
   int   fd;
   char  buff[BUFF_SIZE];

   if ( -1 == mkfifo( FIFO_FILE, 0666))                    // fifo 파일 생성
   {
      perror( "mkfifo() run error");
      exit( 1);
   }

   if ( -1 == ( fd = open( FIFO_FILE, O_RDWR)))           //  fifo 파일 열기
   {
      perror( "open() error");
      exit( 1);
   }

   while( 1 )
   {
      memset( buff, 0, BUFF_SIZE);
      read( fd, buff, BUFF_SIZE);                             //  fifo 파일 읽기
      printf( "%d: %s\n", counter++, buff);
      if( buff[0]=='q')
      {
	      close(fd);
	      exit(0);
      }
   }
   close( fd);
}
