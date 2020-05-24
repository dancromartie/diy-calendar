A simple command-line calendar (~200 LOC)

Events are plain text files:

```
$ cat events/a_bday

name: a_bday
date: 2020-10-09
start_time: 01:01
duration_minutes: 1
notes: born in 1946
recurs: annually
recurs_until: 2099-01-01
```

```
$ cat events/india_flight

name: india_flight
date: 2020-09-15
start_time: 18:00
duration_minutes: 600
notes: flight 55954
```

Add event:

```
./add_event.py --name joes_bday --date 2020-08-01 --start-time 01:01 \
    --recurs annually --recurs-until 2099-01-01
```

See upcoming events:

```
$ ./whats_next.py

2020-05-24 (Sun), 13:00, dentist_may_2020 (in -1 days)
2020-06-02 (Tue), 00:01, b_bday (in 8 days)
2020-09-15 (Tue), 18:00, india_flight (in 113 days)
2020-10-09 (Fri), 01:01, a_bday (in 137 days)
2021-05-20 (Thu), 00:01, c_bday (in 360 days)
2021-06-02 (Wed), 00:01, b_bday (in 373 days)
2021-10-09 (Sat), 01:01, a_bday (in 502 days)
2022-05-20 (Fri), 00:01, c_bday (in 725 days)
```

See upcoming birthdays:

```
./whats_next.py | grep bday
```

To remove an event, use "rm".

To change the time of an event, edit the text file.
