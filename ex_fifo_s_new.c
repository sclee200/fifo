#include <sys/types.h>               // 헤더 파일
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>


#include <pthread.h>


//#define FIFO_FILE "/tmp/fifo"
#define FIFO_FROM_YOLO "/tmp/from_yolo_fifo"
#define FIFO_TO_YOLO "/tmp/to_yolo_fifo"


#define BUFF_SIZE 1024

char buff_s[BUFF_SIZE];
char buff_r[BUFF_SIZE];

int fd_from_yolo;
int fd_to_yolo;

// 쓰레드 함수
void *t_function(void *data)
{
   while(1)
   {
      while(read(fd_from_yolo, buff_r, BUFF_SIZE) != 0)
      {
         //write( handle, buff, 1 );
         printf("%s\n", buff_r);
         memset(buff_r, 0x00, BUFF_SIZE);
      }
   }
}

int main( void)
{
    pthread_t p_thread;
    int thr_id;
    char a[40];

    // 쓰레드 생성 아규먼트로 1 을 넘긴다. 
    thr_id = pthread_create(&p_thread, NULL, t_function, (void *)NULL);
    if (thr_id < 0)
    {
        perror("thread create error : ");
        exit(0);
    }

    // from wifi thread
    if ( -1 == ( fd_from_yolo = open(FIFO_FROM_YOLO, O_RDWR) ))
    {
        if ( -1 == mkfifo( FIFO_FROM_YOLO, 0666))
        {
            perror( "mkfifo() run error");
            //exit( 1);
        }

        if ( -1 == ( fd_from_yolo = open( FIFO_FROM_YOLO, O_RDWR)))
        {
            perror( "open() error");
            //exit( 1);
        }
    }

    // to wifi thread
    if ( -1 == (fd_to_yolo = open( FIFO_TO_YOLO, O_RDWR)))
    {
        if ( -1 == mkfifo(FIFO_TO_YOLO, 0666))
        {
            perror("mkfifo() run error");
            //exit( 1);
        }

        if ( -1 == (fd_to_yolo = open( FIFO_TO_YOLO, O_RDWR)))
        {
            perror( "open() error");
            //exit( 1);
        }
    }

    while(1)
    {
        scanf("%s", buff_s);
        write( fd_to_yolo, buff_s, strlen(buff_s));
        printf("%s send\n", buff_s);

        if(buff_s[0] == 'q')
           break;
    }
    close(fd_from_yolo);
    close(fd_to_yolo);
    sleep(2);
    system("rm -rf /tmp/tmp/from_yolo_fifo");
    system("rm -rf /tmp/tmp/to_yolo_fifo");
}
