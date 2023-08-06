# a tool generate fake data (json or csv) to kafka

```bash
docker run -ti --rm -v $PWD/config.yml:/ws/config.yml --net=host dormi330/bigdata-fake-data:latest
```

# how to use

## use in python

```python
from faker_to_kafka import FakeDataKafkaSender

FakeDataKafkaSender("config.yml")
```

## use in docker
```bash
docker run -ti --rm -v $PWD/config.yml:/ws/config.yml --net=host dormi330/bigdata-fake-data:latest
```

# config.yml description

```yaml
kafka:
  topic: topic01
  bootstrap_servers: 10.201.0.82:9092,10.201.0.83:9092,10.201.0.84:9092

fake:
  locale: en_US

# json | csv
format: json

# 0 = unlimited, how many rows you want to produce
max: 3
# produce frequency, float, like 0.5=0.5row in 1 second
frequency: 1

fields:
  # case1: field_name=country, provider=country, args=None
  - country

  # case2: field_name=date, provider=date, args=%Y-%m-%d %H:%M:%S
  - date1: date

  # case3: field_name=data2, provider=date, args={ pattern="%Y-%m-%d %H:%M:%S" }
  - data2: date
    pattern: "%Y-%m-%d %H:%M:%S"

  # case3: many args
  - id: pyint
    min_value: 1
    max_value: 10
    step: 1
```

# reference

- https://faker.readthedocs.io/en/master/providers/faker.providers.python.html
- https://zhuanlan.zhihu.com/p/87203290
- https://www.cnblogs.com/yunlongaimeng/p/15415783.html