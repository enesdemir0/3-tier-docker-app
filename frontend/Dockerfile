# Stage 1: Build the React app
FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app with Nginx
FROM nginx:stable-alpine
# Copy the built files from Stage 1 to Nginx
COPY --from=build /app/dist /usr/share/nginx/html
# Expose port 80 (Standard for Frontend)
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]