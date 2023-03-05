# FROM alpine:3.17.2 as build
# RUN apk update && apk add zip curl
# RUN curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/110.0.5481.30/chromedriver_linux64.zip" && \
#     curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1070081%2Fchrome-linux.zip?alt=media" && \
#     unzip /tmp/chromedriver.zip -d /opt/ && \
#     unzip /tmp/chrome-linux.zip -d /opt/

FROM public.ecr.aws/lambda/python:3.9
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y && yum clean all
# COPY --from=build /opt/chrome-linux /opt/chrome
# COPY --from=build /opt/chromedriver /opt/
COPY requirements.txt  .
RUN  pip3 install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY .  .
CMD [ "main.handler" ]