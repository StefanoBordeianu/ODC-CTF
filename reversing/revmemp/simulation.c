#include <stdio.h>
#include <stdlib.h>

int main(){
    int random;
    
    srand(0x1337);
    for(int i =0; i<0x21; i++){
        random = rand();
        printf("%d ----> %x\n",i,((random % 0x539) + 0x008 ));
    }

    return 1;
}