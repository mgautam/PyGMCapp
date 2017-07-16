#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <pthread.h>

pthread_mutex_t jobs_queue_mutex;
int jobs_queue_length=0;
char jobs_queue_strings[100][100];

void *worker_thread_func(void* null) {
    int pipeout;
    char rcvbuf[96]={0};
    char cmdbuf[100] = { 0 };
    char responsebuf[100] = { 0 };

    int cmdpos=0;

    while(true) {
        int jobid;
        //extract command from queue
        if (jobs_queue_length > 0) {
            memset(rcvbuf,0,96);
            pthread_mutex_lock(&jobs_queue_mutex);
            jobid=jobs_queue_length;
            strcpy(rcvbuf, jobs_queue_strings[--jobs_queue_length]);
            memset(jobs_queue_strings[jobs_queue_length],0,100);
            pthread_mutex_unlock(&jobs_queue_mutex);

            if(strcmp(rcvbuf,"send_status")==0) {
                sleep(1);//simulating data reception from controller
                //strcpy(responsebuf,"[-4096,-4096,128,8192,1.0]");
                sprintf(responsebuf,"[%5d,%5d,%3d,%4d,%4.2f]",cmdpos,cmdpos,128,8192,1.0);
                printf("id:%d, response: %s\n", jobid, responsebuf); //Print the response

                //send response messages
                pipeout = open("/tmp/cppipe",O_WRONLY);
                write(pipeout, responsebuf, strlen(responsebuf));
                close(pipeout);
            } else {
                strcpy (cmdbuf,"var=");
                strcat (cmdbuf, rcvbuf);
                if(strcmp(rcvbuf,"-409600")==0) cmdpos=-4096;
                else cmdpos=4096;
                sleep(1);//Send command to controller
                printf("id:%d, cmd:%s\n", jobid, cmdbuf);
          }
        } else usleep(10000);
    }
    pthread_exit(NULL);
}

int main(int argc, char **argv) {
    pthread_t worker_thread;

    if (pthread_create(&worker_thread, NULL, worker_thread_func, NULL)) {
      printf("ERROR: return code from pthread_create()\n");
      exit(-1);
    }

    int pipein;

    char rcvbuf[96]={0};

    int jobid;
    int bytes_read;
    while (true) {
        // read data from the gateway server
        pipein = open("/tmp/pcpipe",O_RDONLY);
        bytes_read = read(pipein, rcvbuf, sizeof(rcvbuf));
        close(pipein);
        if( bytes_read > 0 ) {
          rcvbuf[bytes_read]='\0';
          //add cmd to queue
          pthread_mutex_lock(&jobs_queue_mutex);
          strcpy(jobs_queue_strings[jobs_queue_length++],rcvbuf);
          jobid=jobs_queue_length;
          pthread_mutex_unlock(&jobs_queue_mutex);
          printf("id:%d, %s\n",jobid,rcvbuf);
        }
        usleep(10000);
    }

   pthread_exit(NULL);
   return 0;
}
