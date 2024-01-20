FROM python

RUN pip3 install --upgrade pip
RUN pip3 install paho-mqtt influxdb sockets datetime

COPY adapter.py /adapter/
WORKDIR /adapter

CMD ["python3", "adapter.py"]
