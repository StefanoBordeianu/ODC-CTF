#include <stdio.h>

int main(){

    char buffer[12] ={
        0xeb, 0x51, 0xb0, 0x13, 0x85, 0xb9, 0x1c,
        0x87, 0xb8, 0x26, 0x8d, 0x07
    };
    char res[50];
    int var = -0x45;

    for(int i=0;i<0xc;i++){
        res[i]= buffer[i] - var;
        var = res[i] + var;
    }

    for(int i=0;i<12;i++){
        printf("%02hhx ",res[i]);
    }
    printf("\n");

    return 1;
}