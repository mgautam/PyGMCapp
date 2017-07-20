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

typedef struct jobs_queue jobs_queue;
struct jobs_queue {
  int jobid;
  char job_string[100];
  jobs_queue *next;
};
jobs_queue *head, *tail;

char ctrlid[10]={0};
char command[15]={0};
char params[10][10]={0};
int numparams=0;
void parseJSON(char *rcvbuf) {
    memset(ctrlid,0,10);
    memset(command,0,15);
    memset(params,0,10*10);
    numparams=0;

    int i;
    int startIndex=-1,length=-1,endIndex=-1;
    for (i=0; i < 100; i++)
        if(rcvbuf[i]=='[')
            startIndex=i+1;
        else if (rcvbuf[i]==']'){
            length=i-startIndex;
            endIndex=i-1;
        }
    //printf("start:%d,length:%d,end:%d\n",startIndex,length,endIndex);
    int paramIndex=0,quoteStartIndex=-1;
    bool quoteStart=false;
    if ((startIndex!=-1) && (length!=-1))
        for (i=startIndex; i < endIndex; i++)
            if(quoteStart) {
                if (rcvbuf[i]=='"') {
                  quoteStart=false;
                  paramIndex++;
                }
                else {
                  if(paramIndex==0)
                    ctrlid[i-quoteStartIndex]=rcvbuf[i];
                  else if(paramIndex==1)
                    command[i-quoteStartIndex]=rcvbuf[i];
                  else
                    params[paramIndex-2][i-quoteStartIndex]=rcvbuf[i];
                }
            }
            else if(rcvbuf[i]=='"') {
                quoteStartIndex=i+1;
                quoteStart=true;
            }
    numparams=paramIndex-1;
}

void *worker_thread_func(void* null) {
    int pipeout;
    char rcvbuf[96]={0};
    char cmdbuf[100] = { 0 };
    char responsebuf[100] = { 0 };

    int cmdpos=0;
    int jobid;
    jobs_queue *temp_pointer;

    while(true) {
        //extract command from queue
        if (jobs_queue_length > 0) {
            memset(rcvbuf,0,96);

            //pthread_mutex_lock(&jobs_queue_mutex);
            strcpy(rcvbuf, head->next->job_string);
            jobid=head->next->jobid;
            --jobs_queue_length;
            temp_pointer=head->next;
            free(head);
            head=temp_pointer;
            //pthread_mutex_unlock(&jobs_queue_mutex);
            printf("work_recvd: id:%d, %s\n",jobid,rcvbuf);
            parseJSON(rcvbuf);
            /*printf("ctrl:%s, cmd:%s, params: ",ctrlid, command);
            int i=0;
            for (i=0; i<numparams; i++)
              printf("%s, ",params[i]);
            printf("\n");*/

            if(strcmp(command,"send_status")==0) {
                usleep(100000);//simulating data reception from controller
                //strcpy(responsebuf,"[-4096,-4096,128,8192,1.0]");
                sprintf(responsebuf,"[%5d,%5d,%3d,%4d,%4.2f]",cmdpos,cmdpos,128,8192,1.0);
                printf("\twork_excd: id:%d, response: %s\n", jobid, responsebuf); //Print the response

                //send response messages
                pipeout = open("/tmp/cppipe",O_WRONLY);
                write(pipeout, responsebuf, strlen(responsebuf));
                close(pipeout);
            }
            else if(strcmp(command,"motion_cmd")==0) {
                strcpy (cmdbuf,"var=");
                strcat (cmdbuf, params[0]);
                if(strcmp(params[0],"-409600")==0) cmdpos=-4096;
                else cmdpos=4096;
                usleep(100000);//Send command to controller
                printf("\twork_excd: id:%d, cmd:%s\n", jobid, cmdbuf);
            }
        } else usleep(10000);
    }
    printf("PTHREAD exit!\n");
    pthread_exit(NULL);
}

int main(int argc, char **argv) {
    head = (jobs_queue *) malloc(sizeof(jobs_queue));

    pthread_t worker_thread;
    if (pthread_create(&worker_thread, NULL, worker_thread_func, NULL)) {
      printf("ERROR: return code from pthread_create()\n");
      exit(-1);
    }

    int pipein;
    char rcvbuf[96]={0};
    int jobid;
    int bytes_read;
    head->next = (jobs_queue *) malloc(sizeof(jobs_queue));
    tail = head->next;

    while (true) {
        // read data from the gateway server
        pipein = open("/tmp/pcpipe",O_RDONLY);
        bytes_read = read(pipein, rcvbuf, sizeof(rcvbuf));
        close(pipein);
        if( bytes_read > 0 ) {
          rcvbuf[bytes_read]='\0';
          //add cmd to queue
          //pthread_mutex_lock(&jobs_queue_mutex);
          strcpy(tail->job_string,rcvbuf);
          tail->jobid=jobs_queue_length;
          tail->next = (jobs_queue *) malloc(sizeof(jobs_queue));
          tail=tail->next;
          //pthread_mutex_unlock(&jobs_queue_mutex);
          printf("work_delgated: id:%d, %s\n",jobs_queue_length,rcvbuf);
          jobs_queue_length++;
        }
        usleep(10000);
    }

   pthread_exit(NULL);
   return 0;
}
