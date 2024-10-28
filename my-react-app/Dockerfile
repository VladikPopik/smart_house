#from build env 
FROM node:18.19.1-alpine as build
WORKDIR /my-react-app
COPY package*.json ./
RUN npm install 
COPY . ./
RUN npm run build
RUN npm run dev
# production
FROM nginx:latest
COPY --from=build /my-react-app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]
# ENTRYPOINT [ "docker build -t vite-app .", "docker run -p 80:80 vite-app"]