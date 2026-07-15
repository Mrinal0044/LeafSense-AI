# Stage 1: Build static assets
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package.json and install project dependencies
COPY frontend/package.json ./
RUN npm install --legacy-peer-deps

# Copy all source files and build the production bundle
COPY frontend/ ./
RUN npm run build

# Stage 2: Serve static files with Nginx
FROM nginx:stable-alpine

# Copy built HTML/JS assets from builder stage to Nginx directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Overwrite Nginx default config with custom router configurations
COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
