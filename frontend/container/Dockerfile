# syntax=docker/dockerfile:1

############################
# Build stage
############################
FROM node:20-alpine AS build

WORKDIR /app

ARG API_URL
ENV API_URL=${API_URL}

COPY rental_system_web/package*.json ./
RUN npm ci

COPY rental_system_web .
RUN npm run build -- --configuration production


############################
# Runtime stage
############################
FROM nginx:alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY container/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist/rental_system_web /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
