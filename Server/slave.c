#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/socket.h>
#include <string.h>
#include "gclibo.h" //by including the open-source header, all other headers are pulled in.

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
    char responsebuf[100] = { 0 };
    char cmdbuf[100] = { 0 };

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
    do{
        cmdsts=true;
        // read data from the client
        sleep(1);//bytes_read = read(client, buf, sizeof(buf));
        //if( bytes_read > 0 ) {
            strcpy (cmdbuf,"var=");
            cmdsts=check(GCmd(g, cmdbuf));		//Send to Galil Controller
            printf("%s\n", cmdbuf);
        //}
    }while(cmdsts);

    if (g)
      GClose(g);//Close Galil

    return 0;
}
