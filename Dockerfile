FROM anasty17/mltb:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

RUN apt-get -qq update && apt-get -qq install -y gnupg2 wget curl jq pv mediainfo megatools

# add mkvtoolnix latest 
RUN wget -q -O - https://mkvtoolnix.download/gpg-pub-moritzbunkus.txt | apt-key add - && \
    wget -qO - https://ftp-master.debian.org/keys/archive-key-10.asc | apt-key add -
RUN sh -c 'echo "deb https://mkvtoolnix.download/debian/ buster main" >> /etc/apt/sources.list.d/bunkus.org.list' && \
    sh -c 'echo deb http://deb.debian.org/debian buster main contrib non-free | tee -a /etc/apt/sources.list'
RUN wget -O /usr/share/keyrings/gpg-pub-moritzbunkus.gpg https://mkvtoolnix.download/gpg-pub-moritzbunkus.gpg && apt update && apt install mkvtoolnix mkvtoolnix-gui -y

#ffmpeg ke through HE-AAC me audio encode ke liye 
RUN apt install fdkaac -y

#Team Drive me upload ke liye up cmd
RUN mkdir .up && wget -P .up/ https://dl.dropboxusercontent.com/s/623vgzzd9ylff6s/1.json && curl -L https://dl.dropboxusercontent.com/s/kxgpsvi4waaxq37/jkshellup1 -o .up/jkup.py && curl -L https://dl.dropboxusercontent.com/s/3waw7va5bppny8z/jkshellupc -o /usr/local/bin/up && chmod +x /usr/local/bin/up

#local host downloader - bot ke storage ki files ko leech ya mirror ke liye http://localhost:8000/
RUN echo "cHl0aG9uMyAtbSBodHRwLnNlcnZlciAyPiB0LnR4dA==" | base64 -d > /usr/bin/l;chmod +x /usr/bin/l
RUN echo "ZWNobyBodHRwOi8vbG9jYWxob3N0OjgwMDAvJChweXRob24zIC1jICdmcm9tIHVybGxpYi5wYXJzZSBpbXBvcnQgcXVvdGU7IGltcG9ydCBzeXM7IHByaW50KHF1b3RlKHN5cy5hcmd2WzFdKSknICIkMSIpCg==" | base64 -d > /usr/bin/g;chmod +x /usr/bin/g

RUN echo "Y2F0IGU=" | base64 -d > /usr/local/bin/e && chmod +x /usr/local/bin/e

#Server Files remove cmd
RUN echo "cm0gLXJmICpta3YgKmVhYzMgKm1rYSAqbXA0ICphYzMgKmFhYyAqemlwICpyYXIgKnRhciAqN3ogKmR0cyAqbXAzICozZ3AgKnRzICpiZG12ICpmbGFjICp3YXYgKm00YSAqbWthICp3YXYgKmFpZmYgKnNydCAqdnh0ICpzdXAgKmFzcyAqc3NhICptMnRzICphdmkgKndlYm0gKndtdiAqd21hICpqcGcgKmpwZWcgKnBuZwplY2hvICJBbGwgU2VydmVyIEZpbGVzIERlbGV0ZWQuIg==" | base64 -d > /usr/local/bin/0 && chmod +x /usr/local/bin/0

# gdrive and index downloader
RUN echo "Z2Rvd24gLS1mdXp6eSAiJDEiIDI+IGdkLnR4dDsgZWNobyAiWW91ciBHRHJpdmUgRmlsZSBEb3dubG9hZGVkIFN1Y2Nlc3NmdWxseS4uLlxuXG4iOyBzZWQgJ3MrVG86IC91c3Ivc3JjL2FwcC8rTmFtZTogK2c7IDFkOzJkOzQsJGQnIGdkLnR4dA==" |base64 -d > /usr/local/bin/gdown_g;chmod +x /usr/local/bin/gdown_g

RUN echo "bmFtZT0kKHB5dGhvbjMgLWMgImV4ZWMoXCJpbXBvcnQgcmUsc3lzXG5mcm9tIHVybGxpYi5wYXJzZSBpbXBvcnQgdW5xdW90ZV9wbHVzXG5wcmludCAoJyVzJyAlIHVucXVvdGVfcGx1cyhzeXMuYXJndlsxXSkucnNwbGl0KCcvJywgMSlbLTFdKVwiKSIgIiQxIik7IGdkb3duIC1PICIkbmFtZSIgIiQxIiAyPiAvZGV2L251bGw7IGVjaG8gIllvdXIgRmlsZSBTdWNjZXNzZnVsbHkgRG93bmxvYWRlZC4uIFxuXG5OYW1lOiAkbmFtZVxuIg==" | base64 -d > /usr/local/bin/gdown_d; chmod +x /usr/local/bin/gdown_d

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

RUN playwright install && playwright install-deps

COPY . .

CMD ["bash", "start.sh"]
