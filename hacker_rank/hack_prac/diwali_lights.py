def perm(n, c):
    return pow(n, c);


MOD_BASE = pow(10, 5);

if __name__ == "__main__":
    test_case_count = int(raw_input());
    while test_case_count > 0:
        print (perm(2, int(raw_input())) - 1)%MOD_BASE;
        test_case_count -= 1;
