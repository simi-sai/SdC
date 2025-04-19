#define ASM

#if defined(ASM)

    #include <stdio.h>

    int _gini(int gini_val){
        int gini_truncado = (int)gini_val;
        int gini_plus = asm_main(gini_truncado);
        return gini_plus;
    }

#elif defined(PY)

    int _gini(int gini_val){
        return gini_val + 1;
    }

#else

    int _gini(int gini_val){
        return gini_val;
    }

#endif