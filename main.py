import itertools

from config import env, NR, N
from model.fitness_functions import *
from selection.rws import *
from selection.sus import *
from model.encoding import *
from model.gen_operators import *
from output import excel
from runner import run_experiment
from datetime import datetime
import time

# Initialize parameters
beta_values = [2, 1.6, 1.4]
c_values = [0.9801, 0.96059601, 0.922744694, 0.904382075]
beta_value_modified = 1.4


if env == 'test':
    fitness_functions = [
        # (FconstALL(100), 'FconstALL'),
        (FH(BinaryEncoder(100)), 'FH'),
        #(Fx2(FloatEncoder(0.0, 10.23, 10)), 'Fx2'),
        # (Fx2(FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fx2_gray'),
        (F5122subx2(FloatEncoder(-5.12, 5.11, 10)), 'F5122subx2'),
        #(F5122subx2(FloatEncoder(-5.12, 5.11, 10, is_gray=True)), 'F5122subx2_gray'),
        # (Fexp(0.25, FloatEncoder(0.0, 10.23, 10)), 'Fexp0.25'),
        # (Fexp(0.25, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp0.25_gray'),
        # (Fexp(1, FloatEncoder(0.0, 10.23, 10)), 'Fexp1'),
        # (Fexp(1, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp1_gray'),
        # (Fexp(2, FloatEncoder(0.0, 10.23, 10)), 'Fexp2'),
        # (Fexp(2, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp2_gray'),
        # (Frastr(7, FloatEncoder(-5.12, 5.11, 10)), 'Frastr'),
        # (Frastr(7, FloatEncoder(-5.12, 5.11, 10, is_gray=True)), 'Frastr_gray'),
        # (Fdeb2(FloatEncoder(0, 1.023, 10)), 'Fdeb2'),
        # (Fdeb2(FloatEncoder(0, 1.023, 10, is_gray=True)), 'Fdeb2_gray'),
        # (Fdeb4(FloatEncoder(0, 1.023, 10)), 'Fdeb4'),
        # (Fdeb4(FloatEncoder(0, 1.023, 10, is_gray=True)), 'Fdeb4_gray'),
    ]
    selection_methods = [
        # (SUS(), 'SUS (n)'),
        (LinearRankingRWS(1.6), 'RWS_linear_test (1.6)'),
        (ExponentialRankingRWS(0.966), 'RWS_exponential_test (0.966)'),
        # (LinearRankingModifiedRWS(beta_value_modified), 'RWS_linear_modified'),
    ]
    gen_operators = [
        (BlankGenOperator, 'no_operators')
    ]
    num_optimal = [
        (0, "no_optim"),
        (1, "1_optim"),
        # (int(N/20), "5per_optim"),
        # (int(N/10), "10per_optim")
    ]
else:
    fitness_functions = [
        (FconstALL(100), 'FconstALL'),
        (FH(BinaryEncoder(100)), 'FH'),
        (Fx2(FloatEncoder(0.0, 10.23, 10)), 'Fx2'),
        (Fx2(FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fx2_gray'),
        (F5122subx2(FloatEncoder(-5.12, 5.11, 10)), 'F5122subx2'),
        (F5122subx2(FloatEncoder(-5.12, 5.11, 10, is_gray=True)), 'F5122subx2_gray'),
        (Fexp(0.25, FloatEncoder(0.0, 10.23, 10)), 'Fexp0.25'),
        (Fexp(0.25, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp0.25_gray'),
        (Fexp(1, FloatEncoder(0.0, 10.23, 10)), 'Fexp1'),
        (Fexp(1, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp1_gray'),
        (Fexp(2, FloatEncoder(0.0, 10.23, 10)), 'Fexp2'),
        (Fexp(2, FloatEncoder(0.0, 10.23, 10, is_gray=True)), 'Fexp2_gray'),
        (Frastr(7, FloatEncoder(-5.12, 5.11, 10)), 'Frastr'),
        (Frastr(7, FloatEncoder(-5.12, 5.11, 10, is_gray=True)), 'Frastr_gray'),
        (Fdeb2(FloatEncoder(0, 1.023, 10)), 'Fdeb2'),
        (Fdeb2(FloatEncoder(0, 1.023, 10, is_gray=True)), 'Fdeb2_gray'),
        (Fdeb4(FloatEncoder(0, 1.023, 10)), 'Fdeb4'),
        (Fdeb4(FloatEncoder(0, 1.023, 10, is_gray=True)), 'Fdeb4_gray'),
    ]
    selection_methods = [
        (LinearRankingRWS(beta_values[0]), 'RWS_linear (2)'),
        (LinearRankingRWS(beta_values[1]), 'RWS_linear (1.6)'),
        (LinearRankingRWS(beta_values[2]), 'RWS_linear (1.4)'),
        (ExponentialRankingRWS(c_values[0]), 'RWS_exponential (0.9801)'),
        (ExponentialRankingRWS(c_values[1]), 'RWS_exponential (0.96059601)'),
        (ExponentialRankingRWS(c_values[2]), 'RWS_exponential (0.922744694)'),
        (ExponentialRankingRWS(c_values[3]), 'RWS_exponential (0.904382075)'),
        (LinearRankingModifiedRWS(beta_value_modified), 'RWS_linear_modified (1.4)'),
    ]
    gen_operators = [
        (BlankGenOperator, 'no_operators'),
        # (Crossover, 'crossover'),
        # (Mutation, 'mutation'),
        # (CrossoverAndMutation, 'crossover_mut')
    ]
    num_optimal = [
        (0, "no_optim"),
        (1, "1_optim"),
        (int(N/20), "5per_optim"),
        (int(N/10), "10per_optim")
    ]

# a list of tuples of parameters for each run that involves a certain fitness function 
# {fitness_func_name: [(tuples with run parameters), (), ..., ()], other_func: [], ...}

experiment_params = {
    (ff, no): [
        (sm, go, (ff_name, sm_name, go_name, no_name))
        for (sm, sm_name) in selection_methods
        for (go, go_name) in gen_operators
        if not (no_name == "no_optim" and go_name == 'no_operators' and ff_name != 'FconstALL')
    ]
    for (no, no_name) in num_optimal
    for (ff, ff_name) in fitness_functions
    if not (ff_name == "FconstALL" and no_name in ["1_optim", "5per_optim", "10per_optim"])
}

# only keeping one list of populations in memory at a time (for one fitness function)
def generate_all_populations_for_fitness_function(ff, no):
    return [ff.generate_population_for_run(run_i, no) for run_i in range(NR)]

def log(x):
    datetime_prefix = str(datetime.now())[:-4]
    print(f'{datetime_prefix} | {x}')

if __name__ == '__main__':
    log('Program start')
    print('----------------------------------------------------------------------')
    start_time = time.time()
    results = []

    experiment_stats_list = []
    for ff, no in itertools.product(fitness_functions, num_optimal):
        if (ff[0], no[0]) not in experiment_params:
            if no[0] == num_optimal[-1][0]:
                excel.write_ff_stats(experiment_stats_list)
                for experiment_stats in experiment_stats_list:
                    del experiment_stats.runs
                    results.append(experiment_stats)

                ff_end_time = time.time()
                ff_name = experiment_params[(ff[0], 0)][0][2][0]
                log(f'{ff_name} experiments finished in {(ff_end_time - ff_start_time):.2f}s')
                experiment_stats_list = []
            continue
        ff_start_time = time.time()

        populations = generate_all_populations_for_fitness_function(ff[0], no[0])
        params = [params + (populations,) for params in experiment_params[(ff[0], no[0])]]
        experiment_stats_list += [run_experiment(*p) for p in params]

        if no[0] == num_optimal[-1][0]:
            excel.write_ff_stats(experiment_stats_list)
            for experiment_stats in experiment_stats_list:
                del experiment_stats.runs
                results.append(experiment_stats)

            ff_end_time = time.time()
            ff_name = experiment_params[(ff[0], no[0])][0][2][0]
            log(f'{ff_name} experiments finished in {(ff_end_time - ff_start_time):.2f}s')
            experiment_stats_list = []

    excel.write_aggregated_stats(results)

    print('----------------------------------------------------------------------')
    end_time = time.time()
    log(f'Program end. Total runtime: {end_time - start_time:.2f}s')

#TEST
# if __name__ == '__main__':
#     print("---------------------------")
#     print("Rastrigin")
#     x = 0
#     fh = FH(BinaryEncoder(7))
#     genotype = np.array([b'0', b'0', b'0', b'1', b'0', b'0', b'1'])
#     print(fh.apply(genotype))
#     # print(fh.apply(b'0')) # raises ValueError
#     print(fh.get_optimal())
#     print(fh.get_phenotype(genotype))
#     # print(fh.get_phenotype(b'1')) # raises ValueError

