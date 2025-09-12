FROM node:18
WORKDIR /app
COPY package.json package-lock.json .
RUN npm ci --legacy-peer-deps
COPY . .
RUN npm run build
RUN npm install --global http-server
CMD ["npx", "-y", "http-server", "-p", "7000", "/app/build"]
