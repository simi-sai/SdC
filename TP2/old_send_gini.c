#include <stdio.h>

extern int asm_main(int);

int _gini(int gini_val){
    int gini_plus = asm_main(gini_val);
    return gini_plus;
}

int main(){
    float gini_actual = 10.0;
    int gini_truncado = (int)gini_actual;
    int gini_plus = _gini(gini_truncado);

    printf("%d",gini_plus);
    
    return 0;
}