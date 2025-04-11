// send_gini.c

#include <stdio.h>
#include "cdecl.h"

// Assembly routine prototype
int PRE_CDECL asm_main(int) POST_CDECL;

double _gini(double gini_val){
    int gini_plus = asm_main(gini_val);
    return (double)gini_plus;
}

int main(){
    while(1); // Loop
    return 0;
}
