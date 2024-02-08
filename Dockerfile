FROM ubuntu:20.04

RUN apt -qq update

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x run.sh
CMD ["bash","start.sh"]
