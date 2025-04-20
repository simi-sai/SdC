extern int asm_main(int);


int _gini(float gini_val){
    int gini_truncado = (int)gini_val;
    int gini_plus = asm_main(gini_truncado);
    return gini_plus;
}