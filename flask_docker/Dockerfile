FROM python:latest

EXPOSE 5000

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y openjdk-17-jdk-headless

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk-amd64/

RUN wget https://gitlab.com/api/v4/projects/5024297/packages/generic/pdftk-java/v3.3.3/pdftk-all.jar

RUN echo "java -jar pdftk-all.jar \$@" > /usr/bin/pdftk

RUN chmod +x /usr/bin/pdftk

RUN export PDFTK_PATH='/usr/bin/pdftk'

RUN pip install -r requirements.txt --no-cache

RUN apt autoclean

CMD ["sh", "launch_server.sh"]
