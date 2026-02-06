A (SpecAug OFF, greedy, seed0, test): 0.1156
C_train (lexicon=train, test): 0.3859
C_all (lexicon=all/oracle, test): 0.0719
D (SpecAug ON, greedy, seed0, test): 0.1109
E (alias of A, SpecAug OFF, test): 0.1156
CV (SpecAug OFF, test) mean±std over n=4: 0.1361436312538714 ± 0.01483651846166267
Protocol-S greedy test CER mean±std: 0.1274 ± 0.0098 (n=8)
Protocol-S train-lex test CER mean±std: 0.0759 ± 0.0070 (n=8)
Protocol-S per-run (subj, seed, greedy_CER, lex_train_CER):
  subj1 seed0: greedy_CER=0.14060726447219069, lex_train_CER=0.08725879682179341
  subj1 seed1: greedy_CER=0.11677071509648126, lex_train_CER=0.06682746878547105
  subj1 seed2: greedy_CER=0.11833144154370034, lex_train_CER=0.06895573212258797
  subj1 seed3: greedy_CER=0.11577752553916004, lex_train_CER=0.07377979568671963
  subj2 seed0: greedy_CER=0.14074914869466515, lex_train_CER=0.08654937570942112
  subj2 seed1: greedy_CER=0.12414869466515323, lex_train_CER=0.07193530079455164
  subj2 seed2: greedy_CER=0.1271282633371169, lex_train_CER=0.0746311010215664
  subj2 seed3: greedy_CER=0.13592508513053347, lex_train_CER=0.07746878547105562
Protocol-S (SpecAug) greedy test CER mean±std: 0.0945 ± 0.0102 (n=2)
Protocol-S (SpecAug) train-lex test CER mean±std: 0.0588 ± 0.0039 (n=2)
Protocol-S (SpecAug) per-run (subj, seed, greedy_CER, lex_train_CER):
  subj1 seed0: greedy_CER=0.08427922814982974, lex_train_CER=0.05490919409761635
  subj2 seed0: greedy_CER=0.1047105561861521, lex_train_CER=0.0627128263337117
Protocol-S (CrossSubject) greedy test CER mean±std: 0.7343 ± 0.0295 (n=2)
Protocol-S (CrossSubject) train-lex test CER mean±std: 0.6730 ± 0.0426 (n=2)
Protocol-S (CrossSubject) per-run (subj, seed, greedy_CER, lex_train_CER):
  subj1to2 seed0: greedy_CER=0.7047389330306469, lex_train_CER=0.715522133938706
  subj2to1 seed0: greedy_CER=0.7637627695800226, lex_train_CER=0.6303916004540295
