FROM ubuntu

COPY work /work
RUN sh /work/init.sh
EXPOSE 80
CMD [ "sh","/work/run.sh" ]