FROM public.ecr.aws/lambda/python:3.9
RUN echo $PWD
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY .  .
CMD [ "main.handler" ]