FROM --platform=linux/arm64 node:22.8.0

# WORKDIR /usr/src/app

# RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
# RUN apt-get install -y nodejs
# RUN npm create vue@latest

WORKDIR /usr/src/app/vue-app

# RUN npm install
RUN npm install axios
# RUN npm run dev -- --host

EXPOSE 5173

CMD npm install && npm run dev -- --host