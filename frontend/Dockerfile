FROM node:18-slim

WORKDIR /app

RUN npm install -g serve

COPY frontend/build ./build

EXPOSE 3000
CMD ["serve", "build", "--listen", "3000"]
