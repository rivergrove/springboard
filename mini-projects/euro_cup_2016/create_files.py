def create_files(n: int):
    for i in range(1,n+1):
        open(f'sql_q{i}_sol.sql','w')