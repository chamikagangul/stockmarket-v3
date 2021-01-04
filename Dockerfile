FROM python:3.8-slim
COPY . /app
WORKDIR /app

# RUN apk add --update curl gcc g++
# RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
# RUN pip install numpy

RUN pip install -r requirements.txt
EXPOSE 3000 
# ENTRYPOINT [ "python" ] 
CMD [ "python app.py" ] 
