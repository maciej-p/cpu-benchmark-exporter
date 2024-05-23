#!/usr/bin/python3
#Python CPU Benchmark Exporter by Maciej Pasiak
#base on Python CPU Benchmark by Alex Dedyura (Windows, macOS, Linux)

import time
from time import strftime, localtime
import platform
import cpuinfo
import argparse
import prometheus_client

def parse_args():
    parser = argparse.ArgumentParser(
        description="Parse CPU Benchmark Exporter arguments"
    )

    parser.add_argument('--port', type=int, default=9123)

    parser.add_argument('--sleep', type=int, default=60)

    parser.add_argument('--benchmark', type=int, default=10000)

    return parser.parse_args()

def timestamp_to_datetime(timestamp):
   return strftime('%Y-%m-%d %H:%M:%S', localtime(timestamp))

if __name__ == "__main__":

    args = parse_args()

    timestamp_string = str(int(time.time()))

    prometheus_client.start_http_server(args.port)

CPU_BENCHMARK_EXPORTER = prometheus_client.Gauge('cpu_benchmark_exporter',
                                       'Hold current CPU Benchmark (seconds)',
                                       ['bench_cpu', 'bench_arch', 'bench_os', 'bench_os_rel', 'bench_sleep', 'bench_type'])

UPDATE_PERIOD = args.sleep

exporter_labels = {}
exporter_labels['bench_cpu'] = cpuinfo.get_cpu_info().get('brand_raw', "Unknown")
exporter_labels['bench_arch'] = cpuinfo.get_cpu_info().get('arch_string_raw', "Unknown")
exporter_labels['bench_os'] = platform.system()
exporter_labels['bench_os_rel'] = platform.release()
exporter_labels['bench_sleep'] = UPDATE_PERIOD

print('Python CPU Benchmark Exporter by Maciej Pasiak')
print('base on Python CPU Benchmark by Alex Dedyura (Windows, macOS(Darwin), Linux)\n')

print('CPU: ' + exporter_labels['bench_cpu'])
print('Arch: ' + exporter_labels['bench_arch'])
print('OS: ' + exporter_labels['bench_os'], exporter_labels['bench_os_rel'])
print('Python: ' + platform.python_version())

print('\nBenchmarking: \n')

benchmark = int(args.benchmark)

while True:
  start = time.perf_counter()

  for i in range(0,benchmark):
    for x in range(1,1000):
      3.141592 * 2**x
    for x in range(1,10000):
      float(x) / 3.141592
    for x in range(1,10000):
      float(3.141592) / x

  end = time.perf_counter()
  duration = (end - start)
  duration = str(round(duration,3))
  timestamp = time.time()

  print(timestamp_to_datetime(timestamp) + ' - (delay ' + str(UPDATE_PERIOD) + ' s) - ' + (duration + ' s'))

  CPU_BENCHMARK_EXPORTER.labels(exporter_labels['bench_cpu'],
                                exporter_labels['bench_arch'],
                                exporter_labels['bench_os'],
                                exporter_labels['bench_os_rel'],
                                exporter_labels['bench_sleep'],
                                'benchmark').set(duration)

  CPU_BENCHMARK_EXPORTER.labels(exporter_labels['bench_cpu'],
                                exporter_labels['bench_arch'],
                                exporter_labels['bench_os'],
                                exporter_labels['bench_os_rel'],
                                exporter_labels['bench_sleep'],
                                'timestamp').set(str(int(timestamp)))
  time.sleep(UPDATE_PERIOD)
