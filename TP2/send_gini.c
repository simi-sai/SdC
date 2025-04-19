int _gini(int gini_val){
    int gini_plus = asm_main(gini_val);
    return gini_plus;
    // return gini_val + 1;
}

int main(){
    int gini_actual = 10;
    printf("%d",_gini(gini_actual));
    return 0;
}