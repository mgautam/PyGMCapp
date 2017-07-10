#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <string.h>
#include "gclibo.h" //by including the open-source header, all other headers are pulled in.
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

GCon g = 0; //var used to refer to a unique Galil connection

//check return code from most Galil gclib calls
bool check(GReturn e) {
    if (e != G_NO_ERROR) {
        printf("ERROR: %d", e);
        return false;
        //if (g)
        //    GClose(g);//Close Galil
    }
    return true;
}

int main(int argc, char **argv) {
    int pipein,pipeout;

    char responsebuf[100] = { 0 };
    char cmdbuf[100] = { 0 };
    char rcvbuf[96]={0};

    check(GVersion(responsebuf, sizeof(responsebuf)));
    printf("Galil gcLib version: %s\n", responsebuf); //Print the library version

    while (check(GOpen("192.168.2.218 -d", &g))==false) {
        printf(" Galil Connect Error\n");
        sleep(1);
    } //Open a connection to Galil, store the identifier in$

    check(GInfo(g, responsebuf, sizeof(responsebuf)));
    printf("info: %s\n", responsebuf); //Print the connection info

    check(GCommand(g, "MG TIME", responsebuf, sizeof(responsebuf), 0)); //Send MG TIME. Because response is ASC$
    printf("response: %s\n", responsebuf); //Print the response

    bool cmdsts;
    int bytes_read;
    do{
        cmdsts=true;
        // read data from the gateway server
        pipein = open("/tmp/pcpipe",O_RDONLY);
        bytes_read = read(pipein, rcvbuf, sizeof(rcvbuf));
        rcvbuf[bytes_read]='\0';
        close(pipein);
        //strcpy(rcvbuf,"409600");
        //bytes_read=6;
        if( bytes_read > 0 ) {
            if(strcmp(rcvbuf,"send_status")==0) {
                int index=0;
                responsebuf[0]='[';
                index++;
                strcpy(cmdbuf,"MG_RPA");
                check(GCommand(g, cmdbuf, responsebuf+index, sizeof(responsebuf)-index, &bytes_read));
                index+=bytes_read-3;
                responsebuf[index]=',';
                index++;
                strcpy(cmdbuf,"MG_TPA");
                check(GCommand(g, cmdbuf, responsebuf+index, sizeof(responsebuf)-index, &bytes_read));
                index+=bytes_read-3;
                responsebuf[index]=',';
                index++;
                strcpy(cmdbuf,"MG_TVA");
                check(GCommand(g, cmdbuf, responsebuf+index, sizeof(responsebuf)-index, &bytes_read));
                index+=bytes_read-3;
                responsebuf[index]=',';
                index++;
                strcpy(cmdbuf,"MG_TDA");
                check(GCommand(g, cmdbuf, responsebuf+index, sizeof(responsebuf)-index, &bytes_read));
                index+=bytes_read-3;
                responsebuf[index]=',';
                index++;
                strcpy(cmdbuf,"MG_MOA");
                check(GCommand(g, cmdbuf, responsebuf+index, sizeof(responsebuf)-index, &bytes_read));
                index+=bytes_read-3;
                responsebuf[index]=']';
                index++;
                responsebuf[index]='\0';

                printf("response: %s\n", responsebuf); //Print the response

                //send response messages
                pipeout = open("/tmp/cppipe",O_WRONLY);
                write(pipeout, responsebuf, index);
                close(pipeout);
            } else {
                strcpy (cmdbuf,"var=");
                strcat (cmdbuf, rcvbuf);
                cmdsts=check(GCmd(g, cmdbuf));		//Send to Galil Controller
            }
                printf("%s\n", cmdbuf);
        }
        usleep(300000);
    }while(cmdsts);

    if (g)
      GClose(g);//Close Galil
   return 0;
}
