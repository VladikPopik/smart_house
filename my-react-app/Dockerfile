#from build env 
FROM node:18.19.1-alpine AS build
COPY package.json package.json
RUN npm install
COPY . .
RUN npm run build
# production
FROM nginx:stable-alpine
COPY --from=build /dist /usr/share/nginx/html
COPY --from=build nginx.conf /etc/nginx/nginx.conf
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]
# ENTRYPOINT [ "docker build -t vite-app .", "docker run -p 80:80 vite-app"]