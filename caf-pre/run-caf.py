#!/usr/bin/python3

import subprocess

def run(turns, compute, post, leave, invite, run=10, clients=1000, befriend=10):
  errout = open('./caf-{}-{}-{}-{}-{}-{}-{}-{}.err'.f(compute, post, leave,
    invite, turns, run, clients, befriend), 'a+', buffering=0)
  stdout = open('./caf-{}-{}-{}-{}-{}-{}-{}-{}.out'.f(compute, post, leave,
    invite, turns, run, clients, befriend), 'a+', buffering=0)
  args = ['./caf-pre', '-t{}'.f(turns), '-m{}'.f(compute), '-p{}'.f(post),
      '-l{}'.f(leave), '-i{}'.f(invite), '-r{}'.f(run), '-c{}'.f(clients),
      '-b{}'.f(befriend)]
  subprocess.call(args, stdout=stdout, stderr=errout, universal_newlines=True)


def main():
  ts = [100,1000,5000,10000]
  for t in ts:
    run(t, 5, 5, 40, 40)
    run(t, 10, 5, 5, 80)
    #scalability
    run(t, 100,0,0,0)
    run(t, 10, 70, 10,10)
    #mailbox
    run(t, 0,80,0,20,10,1000,100)
    #message
    run(t, 0,0,100,0)
    #actor gc
    run(t, 40,30,5,25,10,1000,50)
    run(t, 1,1,1,97)


if __name__ == '__main__':
  main()

