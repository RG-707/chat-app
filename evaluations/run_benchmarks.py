#!/usr/bin/python

from subprocess import Popen
from subprocess import call
from time import sleep

def run_caf_benchmark(scenario, num_cores, directories, clients, compute, post, leave, invite, befriend, turns=2000, run=10):
    error = open('./caf/{}.err'.format(scenario), 'a+')
    output = open('./caf/{}.out'.format(scenario), 'a+')

    output.write('{}, '.format(num_cores))
    output.flush()
    print(scenario)
    run_cmd = '../caf/build/bin/caf -r {} -t {} -d {} -c {} -m {} -p {} -l {} -i {} -b {} -P --scheduler.max-threads={}'.format(run,
            turns, directories, clients, compute, post, leave, invite, befriend, num_cores)
    print(run_cmd)
    p = Popen(run_cmd, shell=True, universal_newlines=True, stdout=output, stderr=error)
    p.wait()


def run_caf18_benchmark(scenario, num_cores, directories, clients, compute, post, leave, invite, befriend, turns=2000, run=10):
    error = open('./caf18/{}.err'.format(scenario), 'a+')
    output = open('./caf18/{}.out'.format(scenario), 'a+')
    
    output.write('{}, '.format(num_cores))
    output.flush()
    print(scenario)
    run_cmd = '../caf-pre/build/caf-pre -r {} -t {} -d {} -c {} -m {} -p {} -l {} -i {} -b {} -P --caf.scheduler.max-threads={}'.format(run,
            turns, directories, clients, compute, post, leave, invite, befriend, num_cores)
    print(run_cmd)
    p = Popen(run_cmd, shell=True, universal_newlines=True, stdout=output, stderr=error)
    p.wait()


def run_erl_benchmark(scenario, num_cores, directories, clients, compute, post, leave, invite, befriend, turns=2000, run=10):
    error = open('./erlang/{}.err'.format(scenario), 'a+')
    output = open('./erlang/{}.out'.format(scenario), 'a+')
    
    output.write('{}, '.format(num_cores))
    output.flush()
    print(scenario)
    run_cmd = '../erlang/_build/default/bin/chatapp -r {} -t {} -d {} -c {} -m {} -p {} -l {} -i {} -b {} -s +A {}'.format(run,
            turns, directories, clients, compute, post, leave, invite, befriend, num_cores)
    print(run_cmd)
    p = Popen(run_cmd, shell=True, universal_newlines=True, stdout=output, stderr=error)
    p.wait()


def run_pony_benchmark(scenario, num_cores, directories, clients, compute, post, leave, invite, befriend, turns=2000, run=10):
    error = open('./pony/{}.err'.format(scenario), 'a+')
    output = open('./pony/{}.out'.format(scenario), 'a+')
    
    output.write('{}, '.format(num_cores))
    output.flush()
    print(scenario)
    run_cmd = '../pony/pony -r {} -t {} -d {} -c {} -m {} -p {} -l {} -i {} -b {} -s --ponynoblock --ponymaxthreads {}'.format(run,
            turns, directories, clients, compute, post, leave, invite, befriend, num_cores)
    print(run_cmd)
    p = Popen(run_cmd, shell=True, universal_newlines=True, stdout=output, stderr=error)
    p.wait()


def run_all_scenarios(num_cores):
    run_erl_benchmark('scalability', num_cores, 24, 1024, 100, 0, 0, 0, 10)
    run_erl_benchmark('mailbox', num_cores, 8, 256, 0, 80, 0, 20, 100)
    run_erl_benchmark('actorgc', num_cores, 8, 2048, 40, 30, 5, 25, 10)
    run_pony_benchmark('scalability', num_cores, 24, 1024, 100, 0, 0, 0, 10)
    run_pony_benchmark('mailbox', num_cores, 8, 256, 0, 80, 0, 20, 100)
    run_pony_benchmark('actorgc', num_cores, 8, 2048, 40, 30, 5, 25, 10)
    run_pony_benchmark('message', num_cores, 1, 2, 0, 0, 100, 0, 100)
    run_caf_benchmark('message', num_cores, 1, 2, 0, 0, 100, 0, 100)
    run_caf18_benchmark('message', num_cores, 1, 2, 0, 0, 100, 0, 100)
    run_caf_benchmark('scalability', num_cores, 24, 1024, 100, 0, 0, 0, 10)
    run_caf18_benchmark('scalability', num_cores, 24, 1024, 100, 0, 0, 0, 10)
    run_caf_benchmark('mailbox', num_cores, 8, 256, 0, 80, 0, 20, 100)
    run_caf18_benchmark('mailbox', num_cores, 8, 256, 0, 80, 0, 20, 100)
    run_caf_benchmark('actorgc', num_cores, 8, 2048, 40, 30, 5, 25, 10)
    run_caf18_benchmark('actorgc', num_cores, 8, 2048, 40, 30, 5, 25, 10)


def main():
    for i in range(4,132,4):
        cmd = './activate_cores {}'.format(i)
        call(cmd, shell=True)
        sleep(1)
        run_all_scenarios(i)


if __name__ == '__main__':
    main()
